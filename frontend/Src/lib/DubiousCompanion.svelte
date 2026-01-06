<script>
  import { onMount, onDestroy } from 'svelte';
  
  export let script;
  
  let isListening = false;
  let syncStatus = "Idle"; // Idle, Listening, Synced, Lost
  let currentMovieTime = 0; // The virtual clock
  let lastSyncTime = Date.now();
  
  // User Settings
  let settings = {
    profanity: 1,
    violence: 1
  };

  const synth = window.speechSynthesis;

  // Mock Sync Function (In reality, this sends audio fingerprint to server)
  const toggleListen = () => {
    isListening = !isListening;
    if (isListening) {
      syncStatus = "Listening...";
      
      // Simulate finding the sync point after 2 seconds
      setTimeout(() => {
        syncStatus = "Synced";
        currentMovieTime = 145.0; // Assume we joined at 2:25
        lastSyncTime = Date.now();
        startInternalClock();
      }, 2000);
    } else {
      syncStatus = "Idle";
    }
  };

  const startInternalClock = () => {
    if (!isListening) return;
    
    requestAnimationFrame(() => {
      const now = Date.now();
      const delta = (now - lastSyncTime) / 1000;
      currentMovieTime += delta;
      lastSyncTime = now;
      
      checkTimeline(currentMovieTime);
      
      if (isListening) startInternalClock();
    });
  };

  const checkTimeline = (time) => {
    // Same logic as Player, but purely audio
    if (!script) return;
    
    // Find event logic... (Simplified for brevity)
    const event = script.timeline.find(e => 
      time >= (e.start_ms / 1000) && 
      time < (e.end_ms / 1000)
    );

    if (event && !synth.speaking) {
      const scores = event.scores || { profanity: 0 };
      if (scores.profanity > settings.profanity) {
         const utter = new SpeechSynthesisUtterance(event.dubious_text);
         synth.speak(utter);
      }
    }
  };
</script>

<div class="flex flex-col items-center justify-center h-full space-y-8 p-6 text-center">
  
  <div class="relative">
    <div class={`w-48 h-48 rounded-full flex items-center justify-center border-4 transition-all duration-500
      ${isListening ? 'border-red-500 shadow-[0_0_50px_rgba(239,68,68,0.5)]' : 'border-gray-700'}`}>
      
      <button on:click={toggleListen} class="text-2xl font-bold uppercase tracking-widest">
        {isListening ? 'Stop' : 'Listen'}
      </button>
      
    </div>
    
    {#if isListening && syncStatus === "Listening..."}
      <div class="absolute inset-0 rounded-full border-4 border-red-500 animate-ping opacity-20"></div>
    {/if}
  </div>

  <div class="space-y-2">
    <h2 class="text-xl font-bold text-gray-300">{script?.meta?.title || "Unknown Signal"}</h2>
    <p class="font-mono text-yellow-500">{syncStatus}</p>
    {#if syncStatus === "Synced"}
      <p class="font-mono text-sm text-gray-500">
        {new Date(currentMovieTime * 1000).toISOString().substr(11, 8)}
      </p>
    {/if}
  </div>

  <div class="w-full max-w-xs bg-gray-900 p-4 rounded-lg">
    <label class="block text-xs uppercase mb-2 text-gray-400">Profanity Shield</label>
    <input type="range" min="0" max="5" bind:value={settings.profanity} class="w-full accent-red-600" />
  </div>

</div>
