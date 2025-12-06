document.addEventListener('DOMContentLoaded', function(){
  document.getElementById('genShop').addEventListener('click', function(){
    const weekStart = document.getElementById('shopWeek').value;
    if(!weekStart){ alert('Choose week start date'); return; }
    fetch('/api/get_shopping?weekStart=' + encodeURIComponent(weekStart)).then(r=>r.json()).then(j=>{
      const out = document.getElementById('shoppingResult');
      out.innerHTML = '';
      if(j.shopping){
        Object.entries(j.shopping).forEach(([name, qty])=>{
          const div = document.createElement('div');
          div.className = 'shopping-item';
          div.innerHTML = `<div>${name}</div><div class="muted">${qty}</div>`;
          out.appendChild(div);
        });
      } else if (j.error) {
        out.textContent = j.error;
      } else {
        out.textContent = 'No items for that week';
      }
    });
  });
});
