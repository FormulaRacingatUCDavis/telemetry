import { e as escape_html, s as store_get, b as ensure_array_like, u as unsubscribe_stores } from "../../../../chunks/index2.js";
import "chart.js/auto";
import "chartjs-adapter-moment";
import { m as mqttDataStr } from "../../../../chunks/mqtt.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    let selectedSignal = "";
    const lineOptions = [
      { key: "dashboard_torque", label: "Torque [Nm]" },
      { key: "inv_motor_speed", label: "Motor Speed [RPM]" },
      { key: "pei_soc", label: "State of Charge [%]" }
    ];
    $$renderer2.push(`<div class="grid"><article data-theme="light"><small><table class="striped"><thead><tr><th scope="col">Source</th><th scope="col">State</th></tr></thead><tbody><tr><th scope="row">Vehicle Control Unit</th><td>${escape_html(store_get($$store_subs ??= {}, "$mqttDataStr", mqttDataStr).vcuState)}</td></tr><tr><th scope="row">Power Electronics Interface</th><td>${escape_html(store_get($$store_subs ??= {}, "$mqttDataStr", mqttDataStr).bmsState)}</td></tr><tr><th scope="row">Motor Controller</th><td>${escape_html(store_get($$store_subs ??= {}, "$mqttDataStr", mqttDataStr).mcState)}</td></tr></tbody><thead><tr><th scope="col">Metric</th><th scope="col">Value</th></tr></thead><tbody><tr><th scope="row">Speed [MPH]</th><td></td></tr><tr><th scope="row">State of Charge [%]</th><td></td></tr><tr><th scope="row">Motor Controller Temperature [C]</th><td></td></tr><tr><th scope="row">Ground Level Voltage [V]</th><td></td></tr></tbody></table></small></article> <article data-theme="light"><canvas></canvas></article></div> <article data-theme="light">`);
    $$renderer2.select(
      {
        value: selectedSignal,
        onchange: () => {
          return;
        }
      },
      ($$renderer3) => {
        $$renderer3.option({ selected: true, disabled: true, value: "" }, ($$renderer4) => {
          $$renderer4.push(`Select`);
        });
        $$renderer3.push(`<!--[-->`);
        const each_array = ensure_array_like(lineOptions);
        for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
          let signal = each_array[$$index];
          $$renderer3.option({ value: signal.key }, ($$renderer4) => {
            $$renderer4.push(`${escape_html(signal.label)}`);
          });
        }
        $$renderer3.push(`<!--]-->`);
      }
    );
    $$renderer2.push(` <canvas></canvas></article>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _page as default
};
