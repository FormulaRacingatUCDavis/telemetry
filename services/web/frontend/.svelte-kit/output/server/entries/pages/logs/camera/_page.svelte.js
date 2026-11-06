import "clsx";
import { ad as ssr_context } from "../../../../chunks/index2.js";
import "plyr";
import { L as LogDisplay } from "../../../../chunks/LogDisplay.js";
function onDestroy(fn) {
  /** @type {SSRContext} */
  ssr_context.r.on_destroy(fn);
}
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let selectedLog = "";
    onDestroy(() => {
    });
    LogDisplay($$renderer2, { source: "camera", log: selectedLog, logPath: "ready" });
    $$renderer2.push(`<!----> <video controls="" playsinline="" style="width: 600px;"></video>`);
  });
}
export {
  _page as default
};
