import './app.css'
import App from './Src/app.svelte'
import { mount } from 'svelte'

// In Svelte 5, we mount, we don't 'new App({...})'. 
// We attach the parasite to the host.
const app = mount(App, {
  target: document.getElementById('app'),
})

export default app
