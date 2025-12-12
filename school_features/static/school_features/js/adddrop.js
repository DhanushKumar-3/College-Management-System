// Simple JS to submit add/drop via AJAX
document.addEventListener('DOMContentLoaded', function(){
  var form = document.getElementById('adddrop-form');
  if(!form) return;
  form.addEventListener('submit', function(e){
    e.preventDefault();
    var formData = new FormData(form);
    fetch(form.action, {method:'POST', body:formData, headers:{'X-Requested-With':'XMLHttpRequest'}})
      .then(r=>r.json()).then(j=>{ alert(JSON.stringify(j)); });
  });
});
