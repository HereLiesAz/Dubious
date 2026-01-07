<script>
  import DubiousPlayer from './lib/DubiousPlayer.svelte';
  import DubiousCompanion from './lib/DubiousCompanion.svelte';
  import DubiousGenerator from './lib/DubiousGenerator.svelte';
  import { exportDubTrack } from './lib/audioExport.js';
  import { FileUp, Play, Mic, RotateCcw, Download, Wand2 } from 'lucide-svelte';

  let mode = "select"; // select, player, companion, generate
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

<div class="scanline"></div>

<main class="min-h-screen w-full bg-dubious-dark text-dubious-light font-mono flex flex-col relative z-10 selection:bg-dubious-red selection:text-black">
  
  <header class="p-6 border-b border-dubious-gray/50 flex justify-between items-center backdrop-blur-sm bg-black/50 sticky top-0 z-50">
    <div class="flex items-center gap-3">
      <div class="w-3 h-3 bg-dubious-red rounded-full animate-pulse shadow-[0_0_10px_#ff003c]"></div>
      <h1 class="text-dubious-red font-bold tracking-[0.3em] text-xl text-glow">DUBIOUS</h1>
    </div>

    {#if scriptData}
      <button 
        on:click={() => exportDubTrack(scriptData, { profanity: 1 })}
        class="flex items-center gap-2 text-xs border border-dubious-red/50 text-dubious-red px-4 py-2 hover:bg-dubious-red hover:text-black transition-all duration-300 uppercase tracking-wider box-glow">
        <Download size={14} />
        Export EDL
      </button>
    {/if}
  </header>

  <div class="flex-grow flex items-center justify-center p-8">
    
    {#if mode === "select"}
      <div class="space-y-8 text-center max-w-xl w-full animate-in fade-in zoom-in duration-500">

        <div class="relative group">
          <div class="absolute -inset-0.5 bg-gradient-to-r from-dubious-red to-purple-600 rounded-lg opacity-30 group-hover:opacity-75 transition duration-500 blur"></div>
          <div class="relative p-10 bg-black border border-dubious-gray rounded-lg hover:border-dubious-red/50 transition duration-300">

            <div class="mb-6 flex justify-center text-dubious-red opacity-80">
              <FileUp size={48} strokeWidth={1} />
            </div>

            <h2 class="text-lg font-bold mb-2 tracking-widest text-white">UPLOAD MANIFEST</h2>
            <p class="text-sm text-gray-500 mb-6 font-light">Drop your .dps file to initiate the simulacrum.</p>

            <input type="file" on:change={handleFiles} class="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-none file:border file:border-dubious-red
              file:text-xs file:font-bold file:uppercase
              file:bg-black file:text-dubious-red
              hover:file:bg-dubious-red hover:file:text-black
              file:transition-all file:duration-300
              cursor-pointer
            "/>
          </div>
        </div>

        {#if scriptData}
          <div class="grid grid-cols-2 gap-6 pt-4">
            <button on:click={() => mode = "player"} class="group relative overflow-hidden bg-black border border-dubious-gray p-6 hover:border-dubious-red transition duration-300">
              <div class="absolute inset-0 bg-dubious-red/5 translate-y-full group-hover:translate-y-0 transition duration-300"></div>
              <div class="relative z-10 flex flex-col items-center gap-3">
                <Play size={32} class="text-dubious-red group-hover:scale-110 transition duration-300" />
                <span class="text-xs uppercase tracking-widest font-bold">Local Player</span>
              </div>
            </button>

            <button on:click={() => mode = "companion"} class="group relative overflow-hidden bg-black border border-dubious-gray p-6 hover:border-dubious-red transition duration-300">
              <div class="absolute inset-0 bg-dubious-red/5 translate-y-full group-hover:translate-y-0 transition duration-300"></div>
              <div class="relative z-10 flex flex-col items-center gap-3">
                <Mic size={32} class="text-dubious-red group-hover:scale-110 transition duration-300" />
                <span class="text-xs uppercase tracking-widest font-bold">Companion Mode</span>
              </div>
            </button>
          </div>
        {:else}
           <button on:click={() => mode = "generate"} class="w-full flex items-center justify-center gap-2 text-xs border border-dubious-gray/50 text-gray-500 px-4 py-4 hover:border-dubious-red hover:text-dubious-red transition-all duration-300 uppercase tracking-wider">
             <Wand2 size={16} />
             Don't have a manifest? Generate one
           </button>
        {/if}
      </div>

    {:else if mode === "generate"}
       <DubiousGenerator />

    {:else if mode === "player"}
      <div class="w-full max-w-4xl animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="bg-black border border-dubious-gray rounded-lg p-1 shadow-2xl box-glow">
          <DubiousPlayer src={videoFile} script={scriptData} />
        </div>
      </div>
      
    {:else if mode === "companion"}
      <div class="w-full max-w-md animate-in fade-in slide-in-from-bottom-4 duration-500">
        <DubiousCompanion script={scriptData} />
      </div>
      
    {/if}
  </div>

  {#if mode !== "select"}
    <button on:click={() => mode = "select"} class="fixed top-24 left-6 md:top-6 md:left-auto md:right-6 flex items-center gap-2 text-xs text-gray-500 hover:text-dubious-red transition-colors opacity-50 hover:opacity-100 z-50 uppercase tracking-widest">
      <RotateCcw size={14} />
      Reset System
    </button>
  {/if}

</main>

<style>
  /* Extra subtle grid background */
  main::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      linear-gradient(rgba(255, 0, 60, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 0, 60, 0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
  }
</style>
