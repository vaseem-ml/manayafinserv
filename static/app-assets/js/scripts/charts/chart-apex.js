/*=========================================================================================
    File Name: chart-apex.js
    Description: Apexchart Examples
    ----------------------------------------------------------------------------------------
    Item Name: Vuexy  - Vuejs, HTML & Laravel Admin Dashboard Template
    Author: PIXINVENT
    Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

$(function () {
  'use strict';

  var flatPicker = $('.flat-picker'),
    isRtl = $('html').attr('data-textdirection') === 'rtl',
    chartColors = {
      column: {
        series1: '#826af9',
        series2: '#d2b0ff',
        bg: '#f8d3ff'
      },
      success: {
        shade_100: '#7eefc7',
        shade_200: '#06774f'
      },
      donut: {
        series1: '#ffe700',
        series2: '#00d4bd',
        series3: '#826bf8',
        series4: '#2b9bf4',
        series5: '#FFA1A1'
      },
      area: {
        series3: '#a4f8cd',
        series2: '#60f2ca',
        series1: '#2bdac7'
      }
    };





  // Bar Chart
  // --------------------------------------------------------------------

  
  var barChartEl = document.querySelector('#bar-chart'),
  barChartConfig = {
    chart: {
      height: 400,
      type: 'bar',
      parentHeightOffset: 0,
      toolbar: {
        show: false
      }
    },
    plotOptions: {
      bar: {
        horizontal: false,
        barHeight: '20%', // Adjust the barHeight value to reduce thickness
        endingShape: 'rounded'
      }
    },
    grid: {
      xaxis: {
        lines: {
          show: false
        }
      },
      padding: {
        top: -15,
        bottom: -10
      }
    },
    colors: window.colors.solid.info,
    dataLabels: {
      enabled: false
    },
    series: [
      {
        data: [700, 350, 480, 600, 210, 550, 150]
      }
    ],
    xaxis: {
      categories: ['MON, 11', 'THU, 14', 'FRI, 15', 'MON, 18', 'WED, 20', 'FRI, 21', 'MON, 23']
    },
    yaxis: {
      opposite: isRtl
    }
  };
  if (typeof barChartEl !== undefined && barChartEl !== null) {
    var barChart = new ApexCharts(barChartEl, barChartConfig);
    barChart.render();
  }

  // var employees = {{ emp_names | tojson | safe }};
  console.log('this is running++++++++++++++===========', emp_names)

  // Donut Chart
  // --------------------------------------------------------------------
  var donutChartEl = document.querySelector('#donut-chart'),
    donutChartConfig = {
      chart: {
        height: 350,
        type: 'donut'
      },
      legend: {
        show: true,
        position: 'right'
      },
      labels: emp_names,
      series: emp_score,
      colors: [
        chartColors.donut.series1,
        chartColors.donut.series5,
        chartColors.donut.series3,
        chartColors.donut.series4
      ],
      dataLabels: {
        enabled: true,
        formatter: function (val, opt) {
          return parseInt(val) + '%';
        }
      },
      plotOptions: {
        pie: {
          donut: {
            labels: {
              show: true,
              name: {
                fontSize: '2rem',
                fontFamily: 'Montserrat'
              },
              value: {
                fontSize: '1rem',
                fontFamily: 'Montserrat',
                formatter: function (val) {
                  return parseInt(val) + ' Cards';
                }
              },
              total: {
                show: true,
                fontSize: '1.5rem',
                label: 'Cards Graph',
                formatter: function (w) {
                  return 'Cards';
                }
              }
            }
          }
        }
      },
      responsive: [
        {
          breakpoint: 992,
          options: {
            chart: {
              height: 380
            }
          }
        },
        {
          breakpoint: 576,
          options: {
            chart: {
              height: 320
            },
            plotOptions: {
              pie: {
                donut: {
                  labels: {
                    show: true,
                    name: {
                      fontSize: '1.5rem'
                    },
                    value: {
                      fontSize: '1rem'
                    },
                    total: {
                      fontSize: '1.5rem'
                    }
                  }
                }
              }
            }
          }
        }
      ]
    };
  if (typeof donutChartEl !== undefined && donutChartEl !== null) {
    var donutChart = new ApexCharts(donutChartEl, donutChartConfig);
    donutChart.render();
  }
});
