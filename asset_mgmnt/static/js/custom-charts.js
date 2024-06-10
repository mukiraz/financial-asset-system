/**
 * Creates a doughnut chart with data fetched from a specified endpoint and attaches it to a specified element.
 * @param {string} endpoint - The URL to fetch data for the chart.
 * @param {string} elementId - The ID of the HTML element where the chart will be rendered.
 */
async function createDoughnutChart(endpoint, elementId) {
  // Check if the element exists in the DOM
  const element = document.getElementById(elementId);
  if (!element) {
    return; // Exit the function if the element does not exist
  }
  const chartContainer = document.getElementById(elementId).parentNode;
  const loadingImage = chartContainer.querySelector('.loading');

  try {
    // Show the loading image
    loadingImage.style.display = 'block';

    // Fetch data from the endpoint
    const response = await fetch(endpoint);
    const responseData = await response.json();
    // Destructure the necessary properties directly from the response data
    const { labels, data, backgroundColor, borderColor } = responseData;

    console.log(responseData);

    // Get the canvas element by its ID
    const ctx = document.getElementById(elementId).getContext('2d');

    // Create a new doughnut chart
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: backgroundColor,
          borderColor: borderColor,
          borderWidth: 1
        }]
      },
      options: {
        cutout: 90,
        animationEasing: "easeOutBounce",
        animateRotate: true,
        animateScale: false,
        responsive: true,
        maintainAspectRatio: true,
        showScale: true,
        legend: false,
        plugins: {
          legend: {
            display: false,
          }
        }
      },
      plugins: [{
        afterDatasetUpdate: function (chart, args, options) {
          const chartId = chart.canvas.id;
          const legendId = `${chartId}-legend`;
          const legendContainer = document.getElementById(legendId);
          
          // Remove existing ul if it exists
          const existingUl = legendContainer.querySelector('ul');
          if (existingUl) {
            legendContainer.removeChild(existingUl);
          }
      
          // Create new ul
          const ul = document.createElement('ul');
          ul.classList.add('list-unstyled', 'row');
          
          // Populate ul with li elements
          for (let i = 0; i < chart.data.datasets[0].data.length; i++) {
            const li = document.createElement('li');
            li.classList.add('col-4', 'col-md-3');
            
            const span = document.createElement('span');
            span.style.backgroundColor = chart.data.datasets[0].backgroundColor[i];
            
            li.appendChild(span);
            li.appendChild(document.createTextNode(chart.data.labels[i]));
            ul.appendChild(li);
          }
          
          // Append new ul to the legend container
          legendContainer.appendChild(ul);
        }
      }]
      
    });
  } catch (error) {
    console.error('Error creating chart:', error);
  } finally {
    // Hide the loading image
    loadingImage.style.display = 'none';
  }
}

// Helper function to convert hex color to RGBA
function hexToRGBA(hex, opacity) {
  let r = parseInt(hex.slice(1, 3), 16),
    g = parseInt(hex.slice(3, 5), 16),
    b = parseInt(hex.slice(5, 7), 16);

  return `rgba(${r},${g},${b},${opacity})`;
}

let chartInstance = null; // Store the chart instance globally


async function createLineChart(endpoint, elementId) {
  try {
    const response = await fetch(endpoint);
    const responseData = await response.json();
    const labels = responseData["labels"];
    const data = responseData["values"];

    const ctx = document.getElementById(elementId).getContext('2d');

    // Destroy the existing chart instance if it exists
    if (chartInstance) {
      chartInstance.destroy();
    }

    var saleGradientBg = ctx.createLinearGradient(5, 0, 5, 100);
    saleGradientBg.addColorStop(0, 'rgba(26, 115, 232, 0.18)');
    saleGradientBg.addColorStop(1, 'rgba(26, 115, 232, 0.02)');

    // Create a new chart instance and store it globally
    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Güncel Değerler',
          data: data,
          backgroundColor: saleGradientBg,
          borderColor: '#1F3BB3',
          borderWidth: 1.5,
          fill: true,
          pointBorderWidth: 1,
          pointRadius: Array.from({ length: data.length }, () => 4),
          pointHoverRadius: Array.from({ length: data.length }, () => 5),
          pointBackgroundColor: Array.from({ length: data.length }, () => "#1F3BB3"),
          pointBorderColor: Array.from({ length: data.length }, () => "#fff"),
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        elements: {
          line: {
            tension: 0.4,
          }
        },
        scales: {
          y: {
            border: {
              display: false
            },
            grid: {
              display: true,
              color: "#F0F0F0",
              drawBorder: false,
            },
            ticks: {
              beginAtZero: false,
              autoSkip: true,
              maxTicksLimit: 4,
              color: "#6B778C",
              font: {
                size: 10,
              }
            }
          },
          x: {
            border: {
              display: false
            },
            grid: {
              display: false,
              drawBorder: false,
            },
            ticks: {
              beginAtZero: false,
              autoSkip: true,
              maxTicksLimit: 7,
              color: "#6B778C",
              font: {
                size: 10,
              }
            }
          }
        },
        plugins: {
          legend: {
            display: false,
          }
        }
      },
      plugins: [{
        afterDatasetUpdate: function (chart, args, options) {
          const chartId = chart.canvas.id;
          var i;
          const legendId = `${chartId}-legend`;
          const ul = document.createElement('ul');
          for (i = 0; i < chart.data.datasets.length; i++) {
            ul.innerHTML += `
                  <li>
                    <span style="background-color: ${chart.data.datasets[i].borderColor}"></span>
                    ${chart.data.datasets[i].label}
                  </li>
                `;
          }
          return document.getElementById(legendId).appendChild(ul);
        }
      }]
    });
  } catch (error) {
    console.error('Error creating chart:', error);
  }
}
