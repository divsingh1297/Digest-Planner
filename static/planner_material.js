// planner_material.js - drag & drop with visual feedback
document.addEventListener('DOMContentLoaded', function(){
  let draggedId = null;
  document.querySelectorAll('.recipe-item').forEach(el=>{
    el.addEventListener('dragstart', function(e){
      draggedId = this.dataset.id;
      e.dataTransfer.setData('text/plain', draggedId);
      setTimeout(()=> this.classList.add('dragging'), 0);
    });
    el.addEventListener('dragend', function(){ this.classList.remove('dragging'); });
  });
  document.querySelectorAll('.meal-slot').forEach(slot=>{
    slot.addEventListener('dragover', function(e){ e.preventDefault(); this.classList.add('over'); });
    slot.addEventListener('dragleave', function(e){ this.classList.remove('over'); });
    slot.addEventListener('drop', function(e){
      e.preventDefault();
      this.classList.remove('over');
      const id = e.dataTransfer.getData('text/plain');
      const dragged = document.querySelector(`[data-id='${id}']`);
      const title = dragged ? dragged.dataset.title : ('Recipe ' + id);
      this.innerHTML = `<span class="placed-chip" data-recipe-id="${id}">${title}</span>`;
    });
  });

  document.getElementById('savePlan').addEventListener('click', function(){
    const weekStart = document.getElementById('weekStart').value;
    if(!weekStart){ alert('Choose week start date'); return; }
    const plan = {};
    document.querySelectorAll('.day-card').forEach(day=>{
      const d = day.dataset.day;
      plan[d] = {};
      day.querySelectorAll('.meal-slot').forEach(ms=>{
        const meal = ms.dataset.meal;
        const placed = ms.querySelector('[data-recipe-id]');
        plan[d][meal] = placed ? placed.dataset.recipeId : null;
      });
    });
    fetch('/api/save_plan', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ weekStart: weekStart, plan: plan })
    }).then(r=>r.json()).then(j=>{
      if(j.status==='ok') alert('Plan saved');
      else alert('Error saving');
    });
  });
});
