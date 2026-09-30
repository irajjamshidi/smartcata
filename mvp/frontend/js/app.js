import {api} from './api.js'; import {render} from './products.js';
const search=document.querySelector('#search'), editor=document.querySelector('#editor');
async function load(){let d=await api.list({search:search.value});render(d.items);document.querySelector('#status').textContent=`${d.total} محصول`}
search.addEventListener('input',load);document.querySelector('#new-product').onclick=()=>editor.showModal();document.querySelector('#export').onclick=api.export;document.querySelector('#save').onclick=async e=>{e.preventDefault();let d=Object.fromEntries(new FormData(editor.querySelector('form')));d.cost=+d.cost||0;d.price=+d.price||0;await api.create(d);editor.close();load()};load();
