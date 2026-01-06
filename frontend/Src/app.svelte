<script>
  import DubiousPlayer from './lib/DubiousPlayer.svelte';
  import DubiousCompanion from './lib/DubiousCompanion.svelte';
  import { exportDubTrack } from './lib/audioExport.js';

  let mode = "select"; // select, player, companion
  let videoFile = null;
  let scriptData = null;

  const handleFiles = async (e) => {
    // Simplistic file handler for demo
    const file = e.target.files[0];
    if (file.name.endsWith('.dps') || file.name.endsWith('.json')) {
      const text = await file.text();
      scriptData = JSON.parse(text);
    } else {
      videoFile = URL.createObjectURL(file);
    }
  };
</script>

<main class="min-h-screen w-screen bg-black text-gray-200 font-mono flex flex-col">
  
  <header class="p-4 border-b border-gray-800 flex justify-between items-center">
    <h1 class="text-red-600 font-bold tracking-[0.2em] text-lg">DUBIOUS</h1>
    {#if scriptData}
      <button 
        on:click={() => exportDubTrack(scriptData, { profanity: 1 })}
        class="text-xs border border-gray-600 px-3 py-1 hover:bg-white hover:text-black transition">
        EXPORT EDL
      </button>
    {/if}
  </header>

  <div class="flex-grow flex items-center justify-center">
    
    {#if mode === "select"}
      <div class="space-y-6 text-center max-w-md">
        <div class="p-6 border border-dashed border-gray-700 rounded-lg space-y-4">
          <p class="text-sm text-gray-500">Drop your .dps file here</p>
          <input type="file" on:change={handleFiles} class="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-gray-800 file:text-white
            hover:file:bg-gray-700
          "/>
        </div>

        {#if scriptData}
          <div class="grid grid-cols-2 gap-4">
            <button on:click={() => mode = "player"} class="bg-gray-800 p-4 hover:bg-gray-700 transition">
              <span class="block text-2xl mb-2">▶️</span>
              <span class="text-xs uppercase">Local Player</span>
            </button>
            <button on:click={() => mode = "companion"} class="bg-gray-800 p-4 hover:bg-gray-700 transition">
              <span class="block text-2xl mb-2">🎙️</span>
              <span class="text-xs uppercase">Companion Mode</span>
            </button>
          </div>
        {/if}
      </div>

    {:else if mode === "player"}
      <DubiousPlayer src={videoFile} script={scriptData} />
      
    {:else if mode === "companion"}
      <DubiousCompanion script={scriptData} />
      
    {/if}
  </div>

  {#if mode !== "select"}
    <button on:click={() => mode = "select"} class="absolute top-4 left-1/2 -translate-x-1/2 text-xs opacity-50 hover:opacity-100">
      RESET
    </button>
  {/if}

</main>
