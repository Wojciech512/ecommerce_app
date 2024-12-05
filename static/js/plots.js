  var dailyLabels = salesData.map(function(item) {
    return item.date.substring(0, 10);
  });
  var dailySales = salesData.map(function(item) {
    return item.total_sales;
  });

  var ctx = document.getElementById('dailySalesChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: dailyLabels,
      datasets: [{
        label: 'Daily Sales ($)',
        data: dailySales,
        borderColor: 'rgba(75, 192, 192, 1)',
        fill: false,
      }]
    },
    options: {
      scales: {
        x: {
          title: {
            display: true,
            text: 'Data'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Sales Amount ($)'
          }
        }
      }
    }
  });

  var monthlyLabels = monthlySalesData.map(function(item) {
    return item.month.substring(0, 7);
  });
  var monthlySales = monthlySalesData.map(function(item) {
    return item.total_sales;
  });

  var ctx2 = document.getElementById('monthlySalesChart').getContext('2d');
  new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: monthlyLabels,
      datasets: [{
        label: 'Monthly Sales ($)',
        data: monthlySales,
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
      }]
    },
    options: {
      scales: {
        x: {
          title: {
            display: true,
            text: 'Miesiąc'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Sales Amount ($)'
          }
        }
      }
    }
  });

  var productLabels = topProducts.map(function(item) {
    return item.product__title;
  });
  var productQuantities = topProducts.map(function(item) {
    return item.total_quantity;
  });

  var ctx3 = document.getElementById('topProductsChart').getContext('2d');
  new Chart(ctx3, {
    type: 'pie',
    data: {
      labels: productLabels,
      datasets: [{
        data: productQuantities,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)'
        ],
      }]
    },
    options: {
      responsive: true,
    }
  });

  var categoryLabels = salesByCategory.map(function(item) {
    return item.product__category__name;
  });
  var categorySales = salesByCategory.map(function(item) {
    return item.total_sales;
  });

  var ctx4 = document.getElementById('salesByCategoryChart').getContext('2d');
  new Chart(ctx4, {
    type: 'doughnut',
    data: {
      labels: categoryLabels,
      datasets: [{
        data: categorySales,
        backgroundColor: [
          'rgba(255, 159, 64, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(75, 192, 192, 0.6)',
        ],
      }]
    },
    options: {
      responsive: true,
    }
  });
