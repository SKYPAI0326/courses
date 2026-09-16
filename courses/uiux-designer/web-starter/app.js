const card = document.querySelector('.task-card');
const button = document.querySelector('#complete-task');
const status = document.querySelector('#task-status');
const feedback = document.querySelector('#feedback');

button.addEventListener('click', () => {
  card.classList.add('is-done');
  status.textContent = '已完成';
  button.textContent = '已完成';
  button.disabled = true;
  feedback.textContent = '確認完成：任務狀態已更新。';
});
