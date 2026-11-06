

export const index = 5;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/live/camera/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/5.CtD3zDAg.js","_app/immutable/chunks/C10nFKEW.js","_app/immutable/chunks/D_a3qmiF.js","_app/immutable/chunks/DClxZEuC.js"];
export const stylesheets = [];
export const fonts = [];
