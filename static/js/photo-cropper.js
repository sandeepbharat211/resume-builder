/**
 * photo-cropper.js
 * ------------------------------------------------------------------
 * Reusable "adjust your photo" widget built on top of Cropper.js.
 *
 * WHY THIS EXISTS
 * When a user picks a photo for their profile or resume, we don't just
 * upload the raw file -- we let them crop/zoom/move it into a nice square
 * first. Cropping happens entirely in the browser (via a <canvas>), and the
 * *already-cropped* image is what gets attached to the file input and
 * uploaded. This guarantees the photo looks exactly the same everywhere
 * it's shown later (profile dropdown, resume preview, and PDF download),
 * because there's only ever one image file involved, not separate
 * display-only crop coordinates that each place would have to reapply.
 *
 * USAGE
 *   initPhotoCropper({
 *     fileInputId:    'id_profile_image',   // the real Django file <input>
 *     modalId:        'photoCropModal',     // Bootstrap modal wrapping the cropper
 *     cropperImageId: 'photoCropperImage',  // <img> Cropper.js attaches to
 *     previewImageId: 'crPhotoPreview',     // small on-page <img> preview (optional)
 *     placeholderId:  'crPhotoPlaceholder', // icon shown when no photo chosen yet (optional)
 *     applyBtnId:     'photoApplyCropBtn',
 *     zoomInBtnId:    'photoZoomInBtn',      // optional
 *     zoomOutBtnId:   'photoZoomOutBtn',     // optional
 *   });
 */
function initPhotoCropper(opts) {
  var fileInput = document.getElementById(opts.fileInputId);
  var modalEl = document.getElementById(opts.modalId);
  var cropperImage = document.getElementById(opts.cropperImageId);
  var previewImage = opts.previewImageId ? document.getElementById(opts.previewImageId) : null;
  var placeholder = opts.placeholderId ? document.getElementById(opts.placeholderId) : null;
  var applyBtn = document.getElementById(opts.applyBtnId);
  var zoomInBtn = opts.zoomInBtnId ? document.getElementById(opts.zoomInBtnId) : null;
  var zoomOutBtn = opts.zoomOutBtnId ? document.getElementById(opts.zoomOutBtnId) : null;

  // If any required element is missing, silently bail instead of throwing --
  // keeps this safe to include on pages that don't use it.
  if (!fileInput || !modalEl || !cropperImage || !applyBtn || typeof Cropper === 'undefined') return;

  var cropper = null;
  var modal = new bootstrap.Modal(modalEl);

  // 1) User picks a file -> read it, show it in the modal, start Cropper.
  fileInput.addEventListener('change', function (e) {
    var file = e.target.files && e.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function (ev) {
      cropperImage.src = ev.target.result;
      modal.show();
    };
    reader.readAsDataURL(file);
  });

  // 2) Once the modal is visible, initialise Cropper.js on the image.
  //    aspectRatio: 1 keeps crops square, which matches how photos are
  //    displayed everywhere in this app (circular avatars).
  modalEl.addEventListener('shown.bs.modal', function () {
    if (cropper) cropper.destroy();
    cropper = new Cropper(cropperImage, {
      aspectRatio: 1,
      viewMode: 1,
      dragMode: 'move',
      autoCropArea: 1,
      background: false,
      cropBoxResizable: true,
      cropBoxMovable: true,
    });
  });

  // Clean up when the modal closes without applying (e.g. Cancel/backdrop click).
  modalEl.addEventListener('hidden.bs.modal', function () {
    if (cropper) { cropper.destroy(); cropper = null; }
  });

  if (zoomInBtn) zoomInBtn.addEventListener('click', function () { if (cropper) cropper.zoom(0.1); });
  if (zoomOutBtn) zoomOutBtn.addEventListener('click', function () { if (cropper) cropper.zoom(-0.1); });

  // 3) "Apply" -> render the crop to a canvas, turn it into a JPEG File,
  //    and swap it into the real file input using DataTransfer (the
  //    standard trick for programmatically setting <input type="file">).
  applyBtn.addEventListener('click', function () {
    if (!cropper) return;
    var canvas = cropper.getCroppedCanvas({
      width: 500,
      height: 500,
      imageSmoothingEnabled: true,
      imageSmoothingQuality: 'high',
    });
    if (!canvas) return;

    canvas.toBlob(function (blob) {
      if (!blob) return;
      var croppedFile = new File([blob], 'photo.jpg', { type: 'image/jpeg' });

      var dt = new DataTransfer();
      dt.items.add(croppedFile);
      fileInput.files = dt.files;

      if (previewImage) {
        previewImage.src = URL.createObjectURL(blob);
        previewImage.style.display = 'block';
      }
      if (placeholder) {
        placeholder.style.display = 'none';
      }

      modal.hide();
    }, 'image/jpeg', 0.92);
  });
}
