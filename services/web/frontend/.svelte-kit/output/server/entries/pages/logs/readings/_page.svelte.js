import { e as escape_html, d as attr, b as ensure_array_like } from "../../../../chunks/index2.js";
import "chart.js/auto";
import "chartjs-adapter-moment";
import { L as LogDisplay } from "../../../../chunks/LogDisplay.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let selectedLog = "";
    let selectedSignal = "";
    let timeElapsed = 0;
    const lineOptions = [
      { key: "dashboard_torque", label: "Torque [Nm]" },
      { key: "inv_motor_speed", label: "Motor Speed [RPM]" },
      { key: "pei_soc", label: "State of Charge [%]" }
    ];
    LogDisplay($$renderer2, { source: "can", log: selectedLog, logPath: "raw" });
    $$renderer2.push(`<!----> <article data-theme="light"><label>Time Elapsed: ${escape_html(timeElapsed)} seconds <input type="range"${attr("value", timeElapsed)} min="0" max="100"/></label> <table class="striped"><thead><tr><th scope="col">Source</th><th scope="col">State</th></tr></thead><tbody><tr><th scope="row">Vehicle Control Unit</th><td></td></tr><tr><th scope="row">Power Electronics Interface</th><td></td></tr><tr><th scope="row">Motor Controller</th><td></td></tr></tbody><thead><tr><th scope="col">Metric</th><th scope="col">Value</th></tr></thead><tbody><tr><th scope="row">Speed [MPH]</th><td></td></tr><tr><th scope="row">State of Charge [%]</th><td></td></tr><tr><th scope="row">Motor Controller Temperature [C]</th><td></td></tr><tr><th scope="row">Ground Level Voltage [V]</th><td></td></tr></tbody></table></article> <article data-theme="light">`);
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
    $$renderer2.push(` <form><fieldset role="group"><input type="number" name="number" placeholder="Minimum [s]" aria-label="Number"/> <input type="number" name="number" placeholder="Maximum [s]" aria-label="Number"/> <input type="submit" value="Graph"/></fieldset></form> <canvas></canvas></article>`);
  });
}
export {
  _page as default
};
