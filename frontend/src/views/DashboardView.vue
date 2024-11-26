<!-- src/views/DashboardView.vue -->
<template>
    <Layout>
      <!-- Main Section -->
      <main class="main-section">
        <section class="data-visualizations">
          <div class="visualization-card">
            <Doughnut v-if="pieChartData" :data="pieChartData" :options="pieChartOptions" style="max-height: 100%; max-width: 100%;"/>
            <p v-else>데이터를 불러오는 중입니다...</p>
          </div>
          <div class="visualization-card">데이터 시각화 2</div>
          <div class="visualization-card">데이터 시각화 3</div>
          <div class="visualization-card">데이터 시각화 4</div>
        </section>
      </main>
    </Layout>
  </template>
  
  <script setup>
  import { Doughnut } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js'
  import { onMounted, ref, computed } from 'vue'
  import { useDashboardStore } from '@/stores/dashboard'
  import Layout from '@/components/Layout.vue'
  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);
  // 스토어 사용
  const dashboardStore = useDashboardStore()
  
  // 컴포넌트가 마운트될 때 데이터 가져오기
  onMounted(() => {
    dashboardStore.fetchData()
  })

  const pieChartData = computed(() => {
    if (dashboardStore.dataVisualization1) {
      const labels = dashboardStore.dataVisualization1.map(item => item.category__name)
      const data = dashboardStore.dataVisualization1.map(item => item.article_count)
      return {
        labels: labels,
        datasets: [
        {
          label: '카테고리별 기사 수',
          data: data,
          backgroundColor: [
            '#FF6F61', // 코랄 레드
            '#6B5B95', // 로얄 퍼플
            '#88B04B', // 올리브 그린
            '#F7CAC9', // 로즈 쿼츠
            '#92A8D1', // 스카이 블루
            '#955251', // 로즈 브라운
            '#B565A7', // 오키드 퍼플
            '#009B77', // 터키옥스 그린
            '#DD4124', // 피에스타 레드
            '#45B8AC', // 아쿠아 그린
            '#EFC050', // 골든 옐로우
            '#5B5EA6', // 블루베리 블루
          ],
        },
      ],
      }
    }
    else {
      return null
    }
  })

  const pieChartOptions = {
    responsive: false,
    maintainAspectRatio: false,
    aspectRatio: 1,
  }  

  const generateColors = (numColors) => {
    const colors = [];
    const colorStep = 360 / numColors; // 색상 간의 간격 설정 (360도 범위 내에서)

    for (let i = 0; i < numColors; i++) {
      const hue = i * colorStep;
      colors.push(`hsl(${hue}, 70%, 60%)`); // HSL 색상으로 생성
    }
    return colors;
  };
  </script>
  
  <style scoped>
  /* 3. 메인 영역의 높이를 1800px로 설정 */
  .main-section {
    padding: 40px 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 1800px; /* 메인 영역 높이 설정 */
  }
  
  /* 4. 데이터 시각화 섹션을 4분할 (좌상, 우상, 좌하, 우하) */
  .data-visualizations {
    display: grid;
    grid-template-columns: 1fr 1fr; /* 두 개의 컬럼 */
    grid-template-rows: 1fr 1fr;    /* 두 개의 로우 */
    gap: 20px;
    width: 100%;
    max-width: 1440px;
    height: 100%; /* 섹션 전체 높이 사용 */
  }
  
  .visualization-card {
    background-color: #FFFFFF;
    border: 1px solid #707070;
    border-radius: 10px;
    height: 100%; /* 그리드 셀에 맞게 높이 조정 */
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 24px;
    color: #000000;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.16);
    transition: transform 0.3s, background-color 0.3s;
  }
  
  .visualization-card:hover {
    transform: scale(1.05);
    background-color: #F0F0F0;
  }
  
  /* 반응형 디자인 */
  @media (max-width: 768px) {
    .data-visualizations {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, 1fr); /* 한 컬럼으로 변경 */
    }
  
    .visualization-card {
      font-size: 20px;
      height: 180px;
    }
  }
  
  @media (max-width: 480px) {
    .data-visualizations {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, 1fr); /* 한 컬럼으로 변경 */
    }
  
    .visualization-card {
      font-size: 18px;
      height: 150px;
    }
  }
  </style>
  