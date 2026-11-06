import { ab as slot } from "../../../chunks/index2.js";
function _layout($$renderer, $$props) {
  $$renderer.push(`<div style="display: flex; gap: 10px;"><a href="/logs/readings"><button class="secondary">Readings</button></a> <a href="/logs/camera"><button class="secondary">Camera</button></a></div> <hr/> <!--[-->`);
  slot($$renderer, $$props, "default", {});
  $$renderer.push(`<!--]-->`);
}
export {
  _layout as default
};
