pdfjsLib.GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

document.getElementById("pdfUpload").addEventListener("change", function (e) {
  const file = e.target.files[0];
  const fileReader = new FileReader();

  fileReader.onload = function () {
    const typedArray = new Uint8Array(this.result);

    pdfjsLib.getDocument(typedArray).promise.then(pdf => {
      pdf.getPage(1).then(page => {
        const scale = 1.5;
        const viewport = page.getViewport({ scale });

        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        document.getElementById("viewer").innerHTML = "";
        document.getElementById("viewer").appendChild(canvas);

        page.render({ canvasContext: context, viewport });

        page.getTextContent().then(textContent => {
          const textLayer = document.createElement("div");
          textLayer.style.position = "absolute";
          textLayer.style.top = "0";
          textLayer.style.left = "0";

          pdfjsLib.renderTextLayer({
            textContent,
            container: textLayer,
            viewport,
            textDivs: []
          });

          document.getElementById("viewer").appendChild(textLayer);
        });
      });
    });
  };

  fileReader.readAsArrayBuffer(file);
});

document.addEventListener("mouseup", async () => {
  const text = window.getSelection().toString().trim();

  if (text.length < 5) return;

  const res = await fetch("http://localhost:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const data = await res.json();
  document.getElementById("result").innerText = data.result;
});
