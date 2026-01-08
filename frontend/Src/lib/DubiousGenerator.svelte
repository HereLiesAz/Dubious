<script>
  import { createEventDispatcher } from 'svelte';
  import { FileVideo, Cpu, Download, AlertTriangle, CheckCircle2 } from 'lucide-svelte';

  const dispatch = createEventDispatcher();

  let file = null;
  let processing = false;
  let progress = 0;
  let status = "Idle";
  let generatedScript = null;
  let videoDuration = 0;

  const handleFile = (e) => {
    const f = e.target.files[0];
    if (f && f.type.startsWith('video/')) {
      file = f;
      // Get duration
      const video = document.createElement('video');
      video.preload = 'metadata';
      video.onloadedmetadata = () => {
        window.URL.revokeObjectURL(video.src);
        videoDuration = video.duration;
      }
      video.src = URL.createObjectURL(file);
    }
  };

  const generate = async () => {
    if (!file) return;
    processing = true;
    progress = 0;
    status = "Uploading to Factory...";

    const formData = new FormData();
    formData.append('video', file);

    try {
        status = "Processing on Backend (This may take a while)...";
        // Simulate a slow progress bar just to show activity
        const interval = setInterval(() => {
             if (progress < 90) progress += 1;
        }, 500);

        const response = await fetch('/api/process', {
            method: 'POST',
            body: formData
        });

        clearInterval(interval);

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || 'Server Error');
        }

        generatedScript = await response.json();
        progress = 100;
        status = "Analysis Complete.";
        processing = false;

    } catch (e) {
        console.error(e);
        status = `Error: ${e.message}`;
        alert(`Factory Connection Failed: ${e.message}\nEnsure backend/server.py is running on port 5000.`);
        processing = false;
        progress = 0;
    }
  };

  const download = () => {
    const blob = new Blob([JSON.stringify(generatedScript, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${file.name.split('.')[0]}.dps`;
    a.click();
  };
</script>

<div class="w-full max-w-xl mx-auto p-6 bg-black border border-dubious-gray rounded-lg shadow-2xl animate-in fade-in slide-in-from-bottom-8">

  {#if !generatedScript}
    <div class="text-center space-y-6">
      <div class="flex justify-center text-dubious-red">
        <Cpu size={64} class={processing ? "animate-pulse" : ""} />
      </div>

      <h2 class="text-xl font-bold uppercase tracking-widest text-white">
        {processing ? "Simulating Neural Link" : "Generate Manifest"}
      </h2>

      {#if !processing}
        <div class="relative group cursor-pointer">
          <div class="absolute -inset-0.5 bg-dubious-red rounded-lg opacity-20 group-hover:opacity-50 transition blur"></div>
          <label class="relative block w-full p-8 border-2 border-dashed border-dubious-gray hover:border-dubious-red rounded-lg cursor-pointer bg-black transition-colors">
            <input type="file" accept="video/*" on:change={handleFile} class="hidden" />
            {#if file}
              <div class="flex flex-col items-center gap-2">
                <FileVideo size={32} class="text-dubious-red" />
                <span class="font-mono text-sm">{file.name}</span>
                <span class="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(1)} MB</span>
              </div>
            {:else}
              <span class="text-gray-500 uppercase text-xs tracking-wider">Select Video Source</span>
            {/if}
          </label>
        </div>

        {#if file}
          <button
            on:click={generate}
            class="w-full py-4 bg-dubious-red text-black font-bold uppercase tracking-[0.2em] hover:bg-white transition-colors shadow-[0_0_15px_#ff003c]"
          >
            Initiate Protocol
          </button>
        {/if}

      {:else}
        <!-- Processing State -->
        <div class="space-y-4">
          <div class="h-2 w-full bg-gray-900 rounded-full overflow-hidden border border-dubious-gray/50">
            <div class="h-full bg-dubious-red transition-all duration-200" style="width: {progress}%"></div>
          </div>
          <p class="font-mono text-xs text-dubious-red animate-pulse">{status}</p>
        </div>
      {/if}
    </div>

  {:else}
    <!-- Complete State -->
    <div class="text-center space-y-6">
      <div class="flex justify-center text-green-500">
        <CheckCircle2 size={64} />
      </div>

      <h2 class="text-xl font-bold uppercase tracking-widest text-white">
        Manifest Generated
      </h2>

      <p class="text-xs text-gray-500 font-mono">
        {generatedScript.timeline.length} hallucinatory events injected.
      </p>

      <button
        on:click={download}
        class="w-full py-4 bg-black border border-dubious-red text-dubious-red hover:bg-dubious-red hover:text-black font-bold uppercase tracking-[0.2em] transition-all flex items-center justify-center gap-3"
      >
        <Download size={20} />
        Download .dps
      </button>

      <button
        on:click={() => dispatch('complete', { script: generatedScript, file: file })}
        class="text-xs text-gray-500 hover:text-white uppercase tracking-widest mt-4 block mx-auto transition-colors"
      >
        Load & Return to System
      </button>
    </div>
  {/if}

</div>
