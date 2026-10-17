/* Revenue & Beyond: builds the client's copy of the pre-engagement pack as a branded Word file.
   Runs in the browser only, from the answers on the page. Needs window.docx (docx 9.7.1, loaded on demand)
   and the schema in <script id="peSchema" type="application/json">. Generated alongside
   tools/rnb-site-pre-engagement-form.py, edit that file's notes before changing this one. */
(function () {
  var TEAL = '0B363B', GREEN = '49E8B0', PURPLE = 'C3A1F8', SKY = '6AD1FA', INK = '1C1C1C', OFF = 'F5F4F0', GREY = '5E6366', WHITE = 'FFFFFF';
  var FONT = 'Arial', W = 9638; // A4 width less 2 cm margins, in twentieths of a point
  var ACC = [GREEN, PURPLE, SKY];

  function bin(url) { return fetch(url).then(function (r) { if (!r.ok) throw new Error(url); return r.arrayBuffer(); }); }

  window.peBuildDocx = function (values) {
    var d = window.docx;
    var schema = JSON.parse(document.getElementById('peSchema').textContent);
    return Promise.all([
      bin('/assets/img/rnb-wordmark-white-green-1200.png'),
      bin('/assets/img/rnb-wordmark-teal-1200.png'),
      bin('/assets/img/rainbow-strip.png')
    ]).then(function (imgs) {
      var wmWG = imgs[0], wmTeal = imgs[1], rainbow = imgs[2];
      var NONE = { style: d.BorderStyle.NONE, size: 0, color: 'FFFFFF' };
      var noB = { top: NONE, bottom: NONE, left: NONE, right: NONE };
      function neo(sh) {
        return { top: { style: d.BorderStyle.SINGLE, size: 10, color: TEAL }, left: { style: d.BorderStyle.SINGLE, size: 10, color: TEAL },
                 bottom: { style: d.BorderStyle.SINGLE, size: 30, color: sh || TEAL }, right: { style: d.BorderStyle.SINGLE, size: 30, color: sh || TEAL } };
      }
      var thin = { style: d.BorderStyle.SINGLE, size: 8, color: TEAL };
      function r(text, o) {
        o = o || {};
        return new d.TextRun({ text: text, font: FONT, size: o.size || 21, bold: !!o.bold, italics: !!o.italics, color: o.color || INK,
          characterSpacing: o.spacing, shading: o.shade ? { type: d.ShadingType.CLEAR, fill: o.shade, color: 'auto' } : undefined });
      }
      function p(runs, o) {
        o = o || {};
        return new d.Paragraph({ children: Array.isArray(runs) ? runs : [runs], keepNext: !!o.keepNext, keepLines: true,
          spacing: { before: o.before || 0, after: o.after || 0, line: o.line || 276 }, alignment: o.align });
      }
      function answerParas(v, size) {
        v = (v || '').replace(/\r/g, '');
        if (!v.trim()) return [p(r(''))];
        return v.split('\n').map(function (line, i, a) { return p(r(line, { size: size || 21 }), { after: i < a.length - 1 ? 60 : 0 }); });
      }
      function box(v, minH) {
        return new d.Table({ width: { size: W, type: d.WidthType.DXA }, columnWidths: [W], layout: d.TableLayoutType.FIXED,
          rows: [new d.TableRow({ height: { value: minH || 700, rule: d.HeightRule.ATLEAST }, children: [
            new d.TableCell({ width: { size: W, type: d.WidthType.DXA }, borders: neo(TEAL),
              shading: { type: d.ShadingType.CLEAR, fill: WHITE, color: 'auto' }, margins: { top: 120, bottom: 120, left: 160, right: 160 },
              children: answerParas(v) })] })] });
      }
      function grid(t) {
        var sum = t.widths.reduce(function (a, b) { return a + b; }, 0);
        var ws = t.widths.map(function (x) { return Math.round(x * W / sum); });
        ws[ws.length - 1] += W - ws.reduce(function (a, b) { return a + b; }, 0);
        var b = { top: thin, bottom: thin, left: thin, right: thin };
        var head = new d.TableRow({ tableHeader: true, cantSplit: true, children: t.head.map(function (h, i) {
          return new d.TableCell({ width: { size: ws[i], type: d.WidthType.DXA }, borders: b, shading: { type: d.ShadingType.CLEAR, fill: TEAL, color: 'auto' },
            margins: { top: 90, bottom: 90, left: 120, right: 120 }, children: [p(r(h.toUpperCase(), { size: 15, bold: true, color: WHITE, spacing: 20 }))] });
        }) });
        var rows = t.rows.map(function (row) {
          return new d.TableRow({ cantSplit: true, height: { value: 480, rule: d.HeightRule.ATLEAST }, children: row.map(function (c, i) {
            var lab = c.text != null;
            var kids = lab ? [p(r(c.text, { bold: true, size: 18 }))].concat(c.hint ? [p(r(c.hint, { size: 16, color: GREY }), { before: 20 })] : [])
                           : answerParas(values[c.k], 19);
            return new d.TableCell({ width: { size: ws[i], type: d.WidthType.DXA }, borders: b, verticalAlign: d.VerticalAlign.CENTER,
              shading: { type: d.ShadingType.CLEAR, fill: lab ? OFF : WHITE, color: 'auto' }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, children: kids });
          }) });
        });
        return new d.Table({ width: { size: W, type: d.WidthType.DXA }, columnWidths: ws, layout: d.TableLayoutType.FIXED, rows: [head].concat(rows) });
      }

      var company = values['01 Company name'] || 'Your business';
      var who = values['01 Your name and title'] || '';
      var today = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
      var body = [];

      // cover band
      body.push(new d.Table({ width: { size: W, type: d.WidthType.DXA }, columnWidths: [W], layout: d.TableLayoutType.FIXED, rows: [new d.TableRow({ children: [
        new d.TableCell({ width: { size: W, type: d.WidthType.DXA }, borders: neo(GREEN), shading: { type: d.ShadingType.CLEAR, fill: TEAL, color: 'auto' },
          margins: { top: 460, bottom: 480, left: 520, right: 520 }, children: [
            new d.Paragraph({ children: [new d.ImageRun({ type: 'png', data: wmWG, transformation: { width: 200, height: 22 } })], spacing: { after: 560 } }),
            p(r('PRE-ENGAGEMENT PACK', { size: 16, bold: true, color: GREEN, spacing: 40 }), { after: 200 }),
            p(r(company, { size: 52, bold: true, color: WHITE }), { line: 300, after: 160 }),
            p(r([who, today].filter(Boolean).join('  ·  '), { size: 21, color: WHITE }), { after: 0 })
          ] })] })] }));
      body.push(p(r('Your answers, as sent to Simon on ' + today + '. Every question is here, including any you skipped, so you can add to or change anything and email the file back to simon@revenueandbeyond.com.', { size: 20, color: GREY }), { before: 280, after: 120, line: 300 }));

      schema.forEach(function (s) {
        var num = (s.n < 10 ? '0' : '') + s.n;
        body.push(p(r(''), { before: 360, keepNext: true }));
        body.push(p([r('SECTION ' + num + ' OF ' + schema.length, { size: 15, bold: true, color: GREY, spacing: 28 })]
          .concat(s.optional ? [r('    '), r(' OPTIONAL ', { size: 15, bold: true, color: TEAL, spacing: 28, shade: PURPLE })] : []), { after: 100, keepNext: true }));
        body.push(p([r(' ' + num + ' ', { size: 36, bold: true, color: TEAL, shade: ACC[(s.n - 1) % 3] }), r('  ' + s.title, { size: 36, bold: true, color: TEAL })], { line: 300, keepNext: true }));
        body.push(p(r(s.intro, { size: 19, color: GREY }), { before: 140, after: 40, line: 290, keepNext: true }));
        body.push(new d.Paragraph({ children: [], keepNext: true, border: { bottom: { style: d.BorderStyle.SINGLE, size: 12, color: TEAL, space: 1 } }, spacing: { after: 40 } }));
        s.items.forEach(function (it) {
          if (it.t === 'f') {
            body.push(p(r(it.l, { bold: true }), { before: 240, after: 90, keepNext: true }));
            body.push(box(values[it.k], it.short ? 520 : 900));
          } else {
            body.push(p(r(it.q, { bold: true }), { before: 240, after: it.hint ? 40 : 90, keepNext: true }));
            if (it.hint) body.push(p(r(it.hint, { size: 17, color: GREY }), { after: 90, keepNext: true }));
            body.push(grid(it));
          }
        });
      });

      // close
      body.push(p(r(''), { before: 480 }));
      body.push(new d.Table({ width: { size: W, type: d.WidthType.DXA }, columnWidths: [W], layout: d.TableLayoutType.FIXED, rows: [new d.TableRow({ cantSplit: true, children: [
        new d.TableCell({ width: { size: W, type: d.WidthType.DXA }, borders: neo(GREEN), shading: { type: d.ShadingType.CLEAR, fill: TEAL, color: 'auto' },
          margins: { top: 400, bottom: 400, left: 520, right: 520 }, children: [
            p(r('Thank you for the honesty.', { size: 34, bold: true, color: WHITE }), { after: 160, line: 300 }),
            p([r('Changed something? Email the updated file to ', { size: 20, color: WHITE }), r('simon@revenueandbeyond.com', { size: 20, bold: true, color: GREEN }), r('.', { size: 20, color: WHITE })], { line: 300, after: 300 }),
            new d.Paragraph({ children: [new d.ImageRun({ type: 'png', data: wmWG, transformation: { width: 160, height: 17 } })] })
          ] })] })] }));

      var footer = new d.Footer({ children: [
        new d.Paragraph({ children: [new d.ImageRun({ type: 'png', data: rainbow, transformation: { width: 642, height: 3 } })], spacing: { after: 100 } }),
        new d.Paragraph({ tabStops: [{ type: d.TabStopType.RIGHT, position: W }], children: [
          r('REVENUE & BEYOND  ·  PRE-ENGAGEMENT PACK', { size: 14, bold: true, color: TEAL, spacing: 24 }),
          new d.TextRun({ children: ['\t', d.PageNumber.CURRENT, ' / ', d.PageNumber.TOTAL_PAGES], font: FONT, size: 16, bold: true, color: TEAL })
        ] })
      ] });
      var header = new d.Header({ children: [new d.Paragraph({ children: [new d.ImageRun({ type: 'png', data: wmTeal, transformation: { width: 120, height: 13 } })] })] });

      var doc = new d.Document({
        creator: 'Revenue & Beyond', title: 'Pre-engagement pack: ' + company,
        background: { color: OFF },
        styles: { default: { document: { run: { font: FONT, size: 21, color: INK } } } },
        sections: [{
          properties: { titlePage: true, page: { size: { width: 11906, height: 16838 }, margin: { top: 1000, bottom: 1100, left: 1134, right: 1134, header: 560, footer: 480 } } },
          headers: { default: header, first: new d.Header({ children: [new d.Paragraph({ children: [] })] }) },
          footers: { default: footer, first: footer },
          children: body
        }]
      });
      return d.Packer.toBlob(doc);
    });
  };
})();
