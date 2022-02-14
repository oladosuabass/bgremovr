const btn = document.getElementById('downloadImage');
    const url = "{{ response }}";

    btn.addEventListener('click', (event) => {
      event.preventDefault();
      console.log('ABC')
      downloadImage(url);
    })


    function downloadImage(url) {
      fetch(url, {
        mode : 'cors',
      })
        .then(response => response.blob())
        .then(blob => {
        let blobUrl = window.URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.download = url.replace(/^.*[\\\/]/, '');
        a.href = blobUrl;
        document.body.appendChild(a);
        a.click();
        a.remove();
      })
    }