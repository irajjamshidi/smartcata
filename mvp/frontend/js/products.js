function element(tag, className, value) {
  const node = document.createElement(tag)
  if (className) node.className = className
  node.textContent = value ?? ''
  return node
}

export function render(items) {
  const products = document.querySelector('#products')
  const cards = items.map((product) => {
    const card = element('article', 'card')
    card.append(
      element('div', 'meta', `${product.brand || '—'} · ${product.category || '—'}`),
      element('h3', '', product.name),
      element('div', 'meta', `SKU: ${product.sku}`),
      element('p', 'price', `${product.price} ${product.currency}`),
    )
    return card
  })
  products.replaceChildren(...(cards.length ? cards : [element('p', '', 'محصولی یافت نشد.')]))
}
