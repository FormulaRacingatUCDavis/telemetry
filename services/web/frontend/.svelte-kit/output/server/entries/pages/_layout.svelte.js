import { a as attr_class, c as clsx, e as escape_html, b as ensure_array_like, d as attr, s as store_get, u as unsubscribe_stores } from "../../chunks/index2.js";
import { m as mqttDataStr } from "../../chunks/mqtt.svelte.js";
function LogButton($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { status, request } = $$props;
    $$renderer2.push(`<button${attr_class(clsx(status === "on" ? "outline contrast" : "contrast"))}>${escape_html(request)}</button>`);
  });
}
function _layout($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    let { children } = $$props;
    let files = [];
    let selectedFiles = [];
    $$renderer2.push(`<header class="container"><nav><ul><li><img src="/logo.svg" alt="FRUCD Logo" style="height:70px; width:auto; padding-top:10px"/></li></ul> <ul><li><a href="/" class="secondary nav-link">Home</a></li> <li><a href="/live/readings" class="secondary nav-link">Live</a></li> <li><a href="/logs/readings" class="secondary nav-link">Logs</a></li> <li><a href="/send" class="secondary nav-link">Send</a></li> <li><details class="dropdown"><summary>Export</summary> <ul dir="rtl">`);
    if (files.length > 0) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<!--[-->`);
      const each_array = ensure_array_like(files);
      for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
        let file = each_array[$$index];
        $$renderer2.push(`<li><label dir="ltr"><input type="checkbox" name="phase"${attr("value", file.file_name)}${attr("checked", selectedFiles.includes(file.file_name), true)}/> ${escape_html(file.file_name)}</label></li>`);
      }
      $$renderer2.push(`<!--]--> <li><input class="secondary" type="button" value="Raw"/></li> <li><input class="secondary" type="button" value="Parsed"/></li>`);
    } else {
      $$renderer2.push("<!--[-1-->");
      $$renderer2.push(`<li>No logs available</li>`);
    }
    $$renderer2.push(`<!--]--></ul></details></li> <li>`);
    LogButton($$renderer2, {
      status: store_get($$store_subs ??= {}, "$mqttDataStr", mqttDataStr).logStatus,
      request: store_get($$store_subs ??= {}, "$mqttDataStr", mqttDataStr).logReq
    });
    $$renderer2.push(`<!----></li> <li><button class="contrast" disabled="">Record Camera</button></li></ul></nav> <hr/> <hgroup><h2>Telemetry Dashboard</h2> <p>Formula Racing at UC Davis</p></hgroup> <hr/></header> <main id="main-content" class="container">`);
    children($$renderer2);
    $$renderer2.push(`<!----></main>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _layout as default
};
