<script>
  import { onMount } from 'svelte';
  import DubiousPlayer from './lib/DubiousPlayer.svelte';
  
  let videoFile = null;
  let scriptFile = null;
  let scriptData = null;

  // Handle Video Upload
  const handleVideoUpload = (e) => {
    const file = e.target.files[0];
    videoFile = URL.createObjectURL(file);
  };

  // Handle DPS Script Upload (The "Soul" file)
  const handleScriptUpload = async (e) => {
    const file = e.target.files[0];
    const text = await file.text();
    scriptData = JSON.parse(text);
  };
</script>

<main class="h-screen w-screen bg-black text-gray-300 flex flex-col items-center justify-center font-mono">
  
  {#if !videoFile}
    <div class="space-y-8 text-center">
      <h1 class="text-4xl font-bold tracking-widest text-red-500">DUBIOUS</h1>
      <p class="text-sm opacity-50">Select your victim.</p>
      
      <div class="flex flex-col gap-4">
        <label class="cursor-pointer bg-gray-800 px-6 py-3 rounded hover:bg-gray-700 transition">
          <input type="file" accept="video/*" class="hidden" on:change={handleVideoUpload} />
          Select Video File
        </label>
        
        <label class="cursor-pointer bg-gray-800 px-6 py-3 rounded hover:bg-gray-700 transition">
          <input type="file" accept=".json,.dps" class="hidden" on:change={handleScriptUpload} />
          Select Dub Script (.dps)
        </label>
      </div>
    </div>
  {:else}
    <DubiousPlayer src={videoFile} script={scriptData} />
  {/if}

</main>
