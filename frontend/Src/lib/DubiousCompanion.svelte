<script>
  import { onMount, onDestroy } from 'svelte';
  import { Mic, Radio, Signal } from 'lucide-svelte';
  
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

<div class="flex flex-col items-center justify-center space-y-10 p-6 text-center w-full">
  
  <div class="relative group">
    <!-- Active Ring -->
    <div class={`absolute inset-0 rounded-full border border-dubious-red/30 transition-all duration-1000 ${isListening ? 'scale-150 opacity-100' : 'scale-100 opacity-0'}`}></div>
    <div class={`absolute inset-0 rounded-full border border-dubious-red/20 transition-all duration-1000 delay-100 ${isListening ? 'scale-[2] opacity-50' : 'scale-100 opacity-0'}`}></div>
    
    <!-- Button -->
    <button
      on:click={toggleListen}
      class={`relative w-48 h-48 rounded-full flex flex-col items-center justify-center border-2 transition-all duration-500 z-10 bg-black
      ${isListening
        ? 'border-dubious-red shadow-[0_0_50px_rgba(255,0,60,0.4)] text-dubious-red'
        : 'border-gray-800 text-gray-500 hover:border-dubious-red/50 hover:text-white'}`}
    >
      {#if isListening}
        <Signal class="animate-pulse mb-2" size={48} />
        <span class="text-xs font-bold uppercase tracking-[0.2em] animate-pulse">Scanning</span>
      {:else}
        <Mic class="mb-2" size={48} />
        <span class="text-xs font-bold uppercase tracking-[0.2em]">Initialize</span>
      {/if}
    </button>
  </div>

  <div class="space-y-4 w-full">
    <div class="p-4 bg-black border border-dubious-gray rounded-lg">
      <h2 class="text-sm font-bold text-gray-400 uppercase tracking-widest mb-1">Target Media</h2>
      <p class="text-xl text-white font-mono text-glow truncate">{script?.meta?.title || "NO SIGNAL"}</p>
    </div>

    <div class="flex justify-between items-center px-4 py-2 border-b border-dubious-gray/30">
      <span class="text-xs text-gray-500 uppercase tracking-widest">Status</span>
      <span class={`font-mono text-sm ${syncStatus === 'Synced' ? 'text-green-500 text-shadow-green' : 'text-yellow-500'}`}>
        {syncStatus.toUpperCase()}
      </span>
    </div>

    {#if syncStatus === "Synced"}
      <div class="flex justify-between items-center px-4 py-2 border-b border-dubious-gray/30 animate-in fade-in">
        <span class="text-xs text-gray-500 uppercase tracking-widest">Offset</span>
        <p class="font-mono text-sm text-dubious-red">
          {new Date(currentMovieTime * 1000).toISOString().substr(11, 8)}
        </p>
      </div>
    {/if}
  </div>

  <div class="bg-gray-900/50 p-4 rounded-lg border border-dubious-gray/30 w-full">
    <label class="block text-xs uppercase mb-3 text-dubious-red tracking-widest font-bold text-left">
      Profanity Shield
    </label>
    <div class="relative flex items-center">
      <div class="w-full h-1 bg-gray-800 rounded-full overflow-hidden">
        <div class="h-full bg-dubious-red" style="width: {(settings.profanity / 5) * 100}%"></div>
      </div>
      <input
        type="range"
        min="0"
        max="5"
        bind:value={settings.profanity}
        class="absolute w-full opacity-0 cursor-pointer h-6"
      />
      <div
        class="absolute w-4 h-4 bg-white rounded-full shadow-[0_0_10px_#ff003c] pointer-events-none transition-all duration-75"
        style="left: calc({(settings.profanity / 5) * 100}% - 8px)"
      ></div>
    </div>
  </div>

</div>
