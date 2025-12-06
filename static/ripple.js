// Simple ripple effect for material buttons and cards
document.addEventListener('click', function(e){
  const target = e.target.closest('.btn, .recipe-item, .card, .appbtn, .fab, .list-item');
  if(!target) return;
  const rect = target.getBoundingClientRect();
  const circle = document.createElement('span');
  const d = Math.max(rect.width, rect.height);
  circle.style.width = circle.style.height = d + 'px';
  circle.style.left = (e.clientX - rect.left - d/2) + 'px';
  circle.style.top = (e.clientY - rect.top - d/2) + 'px';
  circle.classList.add('ripple');
  target.appendChild(circle);
  setTimeout(()=> circle.remove(), 600);
});
// add CSS for ripple dynamically
const style = document.createElement('style');
style.innerHTML = `
.ripple{position:absolute;border-radius:50%;transform:scale(0);animation:ripple 600ms linear;background:rgba(255,255,255,0.6);pointer-events:none}
.btn, .recipe-item, .card, .appbtn, .fab, .list-item{position:relative;overflow:hidden}
@keyframes ripple{to{transform:scale(2);opacity:0}}`;
document.head.appendChild(style);
