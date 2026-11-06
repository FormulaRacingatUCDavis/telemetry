import { b as ensure_array_like, e as escape_html } from "./index2.js";
function LogDisplay($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { source, log, logPath } = $$props;
    let files = [];
    function formatTime(ts) {
      return new Date(ts * 1e3).toLocaleString();
    }
    function formatSize(bytes) {
      if (bytes < 1024) return `${bytes} B`;
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
      return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
    }
    async function updateDropdown() {
      const res = await fetch(`/api/${source}/logs/list/${logPath}`);
      const data = await res.json();
      files = data;
    }
    $$renderer2.push(`<article data-theme="light">`);
    $$renderer2.select({ value: log, onfocus: updateDropdown }, ($$renderer3) => {
      $$renderer3.option({ selected: true, disabled: true, value: "" }, ($$renderer4) => {
        $$renderer4.push(`Select`);
      });
      if (files.length > 0) {
        $$renderer3.push("<!--[0-->");
        $$renderer3.push(`<!--[-->`);
        const each_array = ensure_array_like(files);
        for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
          let file = each_array[$$index];
          $$renderer3.option({ value: file.file_name }, ($$renderer4) => {
            $$renderer4.push(`${escape_html(file.file_name)}`);
          });
        }
        $$renderer3.push(`<!--]-->`);
      } else {
        $$renderer3.push("<!--[-1-->");
      }
      $$renderer3.push(`<!--]-->`);
    });
    $$renderer2.push(` <hr/> <small><div class="overflow-auto" style="max-height: 300px;"><table><thead><tr><th>Filename</th><th>Date Created</th><th>Size</th></tr></thead><tbody><!--[-->`);
    const each_array_1 = ensure_array_like(files);
    for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
      let file = each_array_1[$$index_1];
      $$renderer2.push(`<tr><th scope="row">${escape_html(file.file_name)}</th><td>${escape_html(formatTime(file.creation_date))}</td><td>${escape_html(formatSize(file.file_size))}</td></tr>`);
    }
    $$renderer2.push(`<!--]--></tbody></table></div></small></article>`);
  });
}
export {
  LogDisplay as L
};
