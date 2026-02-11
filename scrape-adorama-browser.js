// This script is meant to be run via browser evaluate on each Adorama page
// Extract structured data from LD+JSON
const extractFn = `() => {
  const scripts = document.querySelectorAll('script[type="application/ld+json"]');
  let price = '', rating = '', reviewCount = '', name = '';
  scripts.forEach(s => {
    try {
      const d = JSON.parse(s.textContent);
      if (d.aggregateRating) {
        rating = d.aggregateRating.ratingValue;
        reviewCount = d.aggregateRating.reviewCount;
      }
      if (d.name) name = d.name;
      if (d.offers) {
        const o = Array.isArray(d.offers) ? d.offers[0] : d.offers;
        price = o.price || o.lowPrice || '';
      }
      if (d['@graph']) d['@graph'].forEach(g => {
        if (g.aggregateRating) {
          rating = g.aggregateRating.ratingValue;
          reviewCount = g.aggregateRating.reviewCount;
        }
        if (g.name && !name) name = g.name;
        if (g.offers) {
          const o = Array.isArray(g.offers) ? g.offers[0] : g.offers;
          if (!price) price = o.price || o.lowPrice || '';
        }
      });
    } catch(e){}
  });
  return JSON.stringify({name, price, rating, reviewCount});
}`;
