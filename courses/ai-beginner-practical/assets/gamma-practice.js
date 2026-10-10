/* Copy the complete visible material, with a selection fallback. */
(function () {
  document.querySelectorAll('[data-gamma-copy]').forEach(function (button) {
    button.addEventListener('click', async function () {
      var source = document.getElementById(button.dataset.gammaCopy);
      var status = button.parentElement.querySelector('[data-copy-status]');
      if (!source) return;
      try {
        await navigator.clipboard.writeText(source.textContent);
        status.textContent = '已複製全文；依這一步的說明貼到指定位置。';
      } catch (error) {
        var temp = document.createElement('textarea');
        temp.value = source.textContent;
        temp.style.position = 'fixed'; temp.style.opacity = '0';
        document.body.appendChild(temp); temp.select();
        var copied = false;
        try { copied = document.execCommand('copy'); } catch (copyError) {}
        temp.remove();
        if (copied) {
          status.textContent = '已複製全文；依這一步的說明貼到指定位置。';
        } else {
          var range = document.createRange(); range.selectNodeContents(source);
          var selection = window.getSelection();
          selection.removeAllRanges(); selection.addRange(range);
          status.textContent = '全文已選取，請按 Ctrl+C／⌘C 複製。';
        }
      }
    });
  });
})();
