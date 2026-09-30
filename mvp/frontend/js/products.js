const value=(field,fallback='—')=>field ?? fallback;

function element(tag, className, content) {
  const node=document.createElement(tag);
  if (className) node.className=className;
  node.textContent=content;
  return node;
}

export function render(items) {
  const products=document.querySelector('#products');
  products.replaceChildren();
  if (!items.length) {
    products.append(element('p', '', 'محصولی یافت نشد.'));
    return;
  }
  for (const product of items) {
    const card=element('article', 'card');
    card.append(
      element('div', 'meta', `${value(product.brand)} · ${value(product.category)}`),
      element('h3', '', value(product.name, '')),
      element('div', 'meta', `SKU: ${value(product.sku, '')}`),
      element('p', 'price', `${value(product.price, '')} ${value(product.currency, '')}`),
    );
    products.append(card);
  }
}
