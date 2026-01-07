<script>
  export let src;
  export let script;
  let video, currentTime;
  let settings = { profanity: 1 }; // User Tolerance
  const synth = window.speechSynthesis;

  $: if (script && currentTime) {
    const event = script.timeline.find(e =>
      currentTime >= e.start_ms/1000 && currentTime < e.end_ms/1000
    );
    if (event && event.scores.p > settings.profanity && !synth.speaking) {
      video.volume = 0.1; // Duck Audio
      const utter = new SpeechSynthesisUtterance(event.dubious);
      synth.speak(utter);
    } else if (!event) {
      video.volume = 1.0; // Restore
    }
  }
</script>

<div class="space-y-4 text-center">
  <div class="relative rounded-lg overflow-hidden border border-dubious-gray shadow-[0_0_20px_rgba(255,0,60,0.1)] group">
    <!-- svelte-ignore a11y-media-has-caption -->
    <video
      bind:this={video}
      {src}
      bind:currentTime
      controls
      class="w-full bg-black"
    ></video>
    <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-dubious-red to-transparent opacity-0 group-hover:opacity-100 transition duration-500"></div>
  </div>

  <div class="bg-gray-900/50 p-4 rounded-lg border border-dubious-gray/30">
    <label for="profanity-slider" class="block text-xs uppercase mb-3 text-dubious-red tracking-widest font-bold">
      Profanity Shield Level: <span class="text-white">{settings.profanity}</span>
    </label>
    <div class="relative flex items-center">
      <div class="w-full h-1 bg-gray-800 rounded-full overflow-hidden">
        <div class="h-full bg-dubious-red" style="width: {(settings.profanity / 5) * 100}%"></div>
      </div>
      <input
        id="profanity-slider"
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
    <div class="flex justify-between text-[10px] text-gray-500 mt-2 uppercase font-mono">
      <span>Puritan</span>
      <span>Anarchist</span>
    </div>
  </div>
</div>
