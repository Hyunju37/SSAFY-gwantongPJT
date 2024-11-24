<!-- src/views/DashboardView.vue -->
<template>
    <Layout>
      <!-- Main Section -->
      <main class="main-section">
        <section class="data-visualizations">
          <div class="visualization-card">데이터 시각화 1</div>
          <div class="visualization-card">데이터 시각화 2</div>
          <div class="visualization-card">데이터 시각화 3</div>
          <div class="visualization-card">데이터 시각화 4</div>
        </section>
      </main>
    </Layout>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useDashboardStore } from '@/stores/dashboard'
  import Layout from '@/components/Layout.vue'
  
  // 스토어 사용
  const dashboardStore = useDashboardStore()
  
  // 컴포넌트가 마운트될 때 데이터 가져오기
  onMounted(() => {
    dashboardStore.fetchData()
  })
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
  