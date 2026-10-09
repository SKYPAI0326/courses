const tasks = [
  { id: 'T01', title: '整理交付包', due: '今天18:00', done: false },
  { id: 'T02', title: '確認活動報名資料並補上聯絡電話', due: '明天12:00', done: false },
  { id: 'T03', title: '更新本週任務說明', due: '星期五17:00', done: false }
];
// 增加示範任務，讓清單有足夠長度可測滾動。
for (let n = 4; n <= 15; n += 1) {
  tasks.push({ id: `T${String(n).padStart(2, '0')}`, title: `核對工作室任務${n}`, due: '本週17:00', done: false });
}
const screens = ['login-screen', 'list-screen', 'detail-screen'];
const dialog = document.querySelector('#confirm-dialog');
const feedback = document.querySelector('#feedback');
let selectedTask = null;
let showDone = false;
let toastTimer;

function showScreen(id) {
  screens.forEach(name => { document.querySelector('#' + name).hidden = name !== id; });
  document.querySelector('#bottom-nav').hidden = id === 'login-screen';
  document.querySelector('#scroll-top').hidden = id !== 'list-screen';
  window.scrollTo(0, 0);
}
function renderList() {
  const list = document.querySelector('#task-list');
  list.replaceChildren();
  const visibleTasks = tasks.filter(task => task.done === showDone);
  document.querySelector('#empty-message').hidden = visibleTasks.length !== 0;
  document.querySelector('#list-title').textContent = showDone ? '已完成清單' : '待處理清單';
  document.querySelector('#pending-tab').setAttribute('aria-current', showDone ? 'false' : 'page');
  document.querySelector('#done-tab').setAttribute('aria-current', showDone ? 'page' : 'false');
  visibleTasks.forEach(task => {
    const card = document.createElement('article'); card.className = 'task-card';
    const copy = document.createElement('div'); copy.className = 'task-copy';
    const title = document.createElement('h3'); title.textContent = task.title;
    const meta = document.createElement('p'); meta.className = 'muted';
    meta.textContent = `${task.done ? '已完成' : '待處理'} · ${task.due}`;
    copy.append(title, meta); card.append(copy);
    if (task.done) {
      const badge = document.createElement('img'); badge.className = 'badge';
      badge.src = 'assets/status-badge.png'; badge.alt = '已完成'; card.append(badge);
    }
    const open = document.createElement('button'); open.type = 'button';
    open.textContent = '檢視詳情'; open.setAttribute('aria-label', '檢視詳情：' + task.title);
    open.addEventListener('click', () => {
      selectedTask = task;
      document.querySelector('#detail-title').textContent = task.title;
      document.querySelector('#detail-due').textContent = '期限：' + task.due;
      const complete = document.querySelector('#complete-task');
      complete.disabled = task.done; complete.textContent = task.done ? '已完成' : '標記完成';
      showScreen('detail-screen');
    });
    card.append(open); list.append(card);
  });
}
function openList(done) {
  showDone = done; renderList(); showScreen('list-screen');
}
document.querySelector('#login-button').addEventListener('click', () => openList(false));
document.querySelector('#back-button').addEventListener('click', () => openList(showDone));
document.querySelector('#pending-tab').addEventListener('click', () => openList(false));
document.querySelector('#done-tab').addEventListener('click', () => openList(true));
document.querySelector('#complete-task').addEventListener('click', () => dialog.showModal());
document.querySelector('#cancel-button').addEventListener('click', () => dialog.close());
document.querySelector('#confirm-button').addEventListener('click', () => {
  if (!selectedTask || selectedTask.done) return;
  selectedTask.done = true; dialog.close(); openList(true);
  feedback.textContent = '任務已完成，已移到已完成清單。';
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { feedback.textContent = ''; }, 4000);
});
dialog.addEventListener('click', event => {
  const box = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
});
document.querySelector('#scroll-top').addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
showScreen('login-screen');
