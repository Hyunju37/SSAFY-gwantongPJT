<!-- src/views/HomeView.vue -->
<template>
  <Layout>
    <div class="main-page">
      <!-- Banner Section -->
      <div class="banner">
        <!-- Category Filter Section -->
        <div class="category-filter">
          <button 
            class="category-button" 
            v-for="category in categories"
            :key="category"
            :class="{ active: activeCategory === category }"
            @click="changeCategory(category)"
          >
            {{ category }}
          </button>
          <!-- Add Category Button -->
          <button class="add-category-button" @click="openCategoryPopup" aria-label="카테고리 추가">➕</button>
        </div>
        
        <!-- Category Popup -->
        <div v-if="isCategoryPopupOpen" class="category-popup">
          <div class="popup-content">
            <button class="close-popup" @click="closeCategoryPopup">✖</button>
            <h3>카테고리 추가</h3>
            <div class="popup-categories">
              <button 
                class="popup-category-button" 
                v-for="category in availableCategories" 
                :key="category"
                @click="addCategory(category)"
              >
                {{ category }}
              </button>
            </div>
          </div>
        </div>

        <!-- Main News Section -->
        <div class="main-news-section">
          <div class="post-cards">
            <!-- Image News Cards -->
            <div 
              v-for="(board, index) in imageNewsBoards" 
              :key="board.id"
              class="post-card image-news-card"
              @click="navigateToNews(board.id)"
            >
              <div 
                class="post-image" 
                :style="{ backgroundImage: board.image ? 'url(' + board.image + ')' : 'url(' + defaultImage + ')' }"
              ></div>
              <div class="post-info">
                <h3 class="post-title">{{ board.title }}</h3>
                <!-- Post Info Bottom: Contains Post Date and Post Meta -->
                <div class="post-info-bottom">
                  <p class="post-date">{{ board.date }}</p>
                  <div class="post-meta">
                    <!-- 좋아요 수: 아이콘과 숫자를 분리하여 버튼으로 변경 -->
                    <div class="like-section">
                      <button class="like-button" @click.stop="likePost(board.id)" aria-label="좋아요">
                        👍
                      </button>
                      <span class="like-count">{{ board.likes }}</span>
                    </div>
                    <!-- 조회수: 아이콘과 숫자를 분리 -->
                    <div class="view-section">
                      <span class="view-icon">👀</span>
                      <span class="view-count">{{ board.views }}</span>
                    </div>
                    <button class="link-button" @click.stop="navigateToNews(`0${index + 1}`, index)">기사 바로가기</button>
                  </div>
                </div>
              </div>
            </div>
            <!-- Ranking Card -->
            <div class="post-card ranking-card">
              <div class="top-list" v-for="(list, idx) in rankingLists" :key="idx">
                <h3><span class="trophy-icon">🏆</span> {{ list.title }}</h3>
                <ol>
                  <li 
                    v-for="(item, i) in list.items" 
                    :key="i" 
                    @click="searchByKeyword(item)"
                    class="ranking-item"
                  >
                    {{ item }}
                  </li>
                </ol>
              </div>
            </div>
          </div>
        </div>

        <!-- Sub News Section -->
        <div class="sub-news-section">
          <!-- State Buttons -->
          <div class="section-state-buttons">
            <button 
              class="state-button" 
              v-for="state in ['최신순', '인기순']" 
              :key="state"
              :class="{ active: activeState === state }"
              @click="activeState = state"
            >
              {{ state }}
            </button>
          </div>
          <!-- News Cards -->
          <div class="news-cards">
            <div 
              v-for="(news, index) in newsCards" 
              :key="news" 
              class="news-card"
              @click="navigateToNews(news.id)"
            >
              <div class="category">{{ news.category }}</div>
              <h2 class="news-title">{{ news.title }}</h2>
              <p class="news-content">{{ news.content }}</p>
              <div class="news-meta">
                <span class="news-date">{{ news.date }}</span>
                <!-- 좋아요 수: 아이콘과 숫자를 분리하여 버튼으로 변경 -->
                <div class="like-section">
                  <button class="like-button" @click.stop="likeNews(index)" aria-label="좋아요">
                    👍
                  </button>
                  <span class="like-count">{{ news.likes }}</span>
                </div>
                <!-- 조회수: 아이콘과 숫자를 분리 -->
                <div class="view-section">
                  <span class="view-icon">👀</span>
                  <span class="view-count">{{ news.views }}</span>
                </div>
                <button class="link-button" @click.stop="navigateToNews(`03`, index)">기사 바로가기</button>
              </div>
              <div class="hash-tags">
                <span class="hash-tag" v-for="tag in news.tags" :key="tag">#{{ tag }}</span>
              </div>
            </div>
          </div>
          <!-- Pagination -->
          <div class="move-to-page">
            <button 
              class="page-arrow left" 
              :class="getPageArrowClass('left')" 
              :disabled="currentPage === 1" 
              @click="changePage('prev')" 
              aria-label="이전 페이지"
            >
              ⬅️
            </button>
            <div class="page-indicator">{{ currentPage }} / {{ totalPages }}</div>
            <button 
              class="page-arrow right" 
              :class="getPageArrowClass('right')" 
              :disabled="currentPage === totalPages" 
              @click="changePage('next')" 
              aria-label="다음 페이지"
            >
              ➡️
            </button>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

  <script setup>
  import { ref, onMounted } from 'vue'
  import { useUserStore } from '@/stores/user'
  import { useBoardStore } from '@/stores/board'
  import { useRouter } from 'vue-router'
  import defaultImage from '@/assets/default_image.png'
  import { useNewsStore } from '@/stores/news'
  import Layout from '@/components/Layout.vue'

  // Vue Router
  const router = useRouter()

  // Stores
  const userStore = useUserStore()
  const boardStore = useBoardStore()

  const newsStore = useNewsStore()

  // Reactive Variables
  const searchQuery = ref('')
  const activeCategory = ref('전체')
  const activeState = ref('최신순')
  const currentPage = ref(1)
  const totalPages = ref(1) // 수정

  // 수정 추가
  // 카테고리 관련 상태 변수
  const categories = ref(['전체', '언어', '경제', '교육', '정치', '문화', '스포츠', 'IT/과학'])
  const availableCategories = ref(['사회', '연예', '환경', '건강', '여행', '자동차']) // 추가 가능한 카테고리 예시
  const isCategoryPopupOpen = ref(false)

  // 수정 추가
  // 카테고리 변경 시 호출되는 함수
  const changeCategory = (category) => {
    activeCategory.value = category
    currentPage.value = 1
    fetchNewsData()
  }

  // 카테고리 팝업 열기
  const openCategoryPopup = () => {
    isCategoryPopupOpen.value = true
  }

  // 카테고리 팝업 닫기
  const closeCategoryPopup = () => {
    isCategoryPopupOpen.value = false
  }

  // 카테고리 추가
  const addCategory = (category) => {
    if (!categories.value.includes(category)) {
      categories.value.push(category)
    }
  }

  // 랭킹 리스트 데이터 상태 변수
  const rankingLists = ref([])

  // 랭킹 리스트 데이터 가져오기
  const fetchRankingLists = async () => {
    // TODO: 실제 API 호출로 데이터 가져오기
    // 임의의 데이터 사용
    rankingLists.value = [
      {
        title: 'Top 3 조회 대학',
        items: ['서울대학교', '연세대학교', '고려대학교']
      },
      {
        title: 'Top 3 관심 전공',
        items: ['컴퓨터공학', '경제학', '심리학']
      }
    ]
  }

  // // Mock Data for Image News Boards
  // const imageNewsBoards = ref([
  //   {
  //     id: 1,
  //     title: '이미지 뉴스 01',
  //     date: '2024-11-21',
  //     likes: 10,
  //     views: 100,
  //     image: defaultImage
  //   },
  //   {
  //     id: 2,
  //     title: '이미지 뉴스 02',
  //     date: '2024-11-20',
  //     likes: 5,
  //     views: 50,
  //     image: defaultImage
  //   }
  // ])

  // // Mock Data for News Cards
  // const newsCards = ref([
  //   {
  //     id: 3,
  //     category: '경제',
  //     title: '경제 뉴스 03',
  //     content: '경제 뉴스 내용 03...',
  //     date: '2024-11-19',
  //     likes: 8,
  //     views: 80,
  //     tags: ['경제', '주식', '시장', '금융', '무역']
  //   },
  //   {
  //     id: 4,
  //     category: '정치',
  //     title: '정치 뉴스 04',
  //     content: '정치 뉴스 내용 04...',
  //     date: '2024-11-18',
  //     likes: 12,
  //     views: 120,
  //     tags: ['정치', '선거', '정책', '국회', '대통령']
  //   },
  //   {
  //     id: 5,
  //     category: '문화',
  //     title: '문화 뉴스 05',
  //     content: '문화 뉴스 내용 05...',
  //     date: '2024-11-17',
  //     likes: 7,
  //     views: 70,
  //     tags: ['문화', '예술', '공연', '전시', '영화']
  //   },
  //   {
  //     id: 6,
  //     category: '스포츠',
  //     title: '스포츠 뉴스 06',
  //     content: '스포츠 뉴스 내용 06...',
  //     date: '2024-11-16',
  //     likes: 15,
  //     views: 150,
  //     tags: ['스포츠', '축구', '야구', '농구', '배구']
  //   }
  // ])

  // 스토어에서 데이터 불러오기
  // 뉴스 데이터 상태 변수
  const imageNewsBoards = ref([])
  const newsCards = ref([])

  // 뉴스 데이터 가져오기
  const fetchNewsData = async () => {
    // TODO: 실제 API 호출로 데이터 가져오기
    // 임의의 데이터 사용
    // console.log(activeCategory.value)
    const newsData = await newsStore.fetchNewsByCategory(activeCategory.value, currentPage.value)
    //console.log(newsData)
    imageNewsBoards.value = newsData.imageNews
    newsCards.value = newsData.newsCards

    // 총 페이지 수 업데이트
    totalPages.value = Math.ceil(newsData.totalCount / 6)
  }

  onMounted(() => {
    boardStore.getBoards()
    // 스토어에서 불러오는 함수
    fetchNewsData()
    fetchRankingLists()
  })

  // 페이지 변경 함수
  const changePage = (direction) => {
    if (direction === 'next' && currentPage.value < totalPages.value) {
      currentPage.value++
      fetchNewsData()
    } else if (direction === 'prev' && currentPage.value > 1) {
      currentPage.value--
      fetchNewsData()
    }
  }

  // Navigation Function
  const navigateToNews = (id) => {
    router.push(`/news-posts/${id}`)
  }

  // Placeholder function for liking a post (to be implemented)
  const likePost = (postId) => {
    // 추후 구현 예정: 로그인 및 1회 좋아요 제한 로직 추가
    console.log(`좋아요 버튼 클릭: 게시물 ID ${postId}`)
  }

  // Placeholder function for liking a news item (to be implemented)
  const likeNews = (newsId) => {
    // 추후 구현 예정: 로그인 및 1회 좋아요 제한 로직 추가
    console.log(`좋아요 버튼 클릭: 뉴스 ID ${newsId}`)
  }

  // Search Function (for ranking items)
  const searchByKeyword = (keyword) => {
    // 추후 구현 예정: 검색 기능 로직 추가
    // console.log(`검색 키워드: ${keyword}`)
    // 예시: router.push(`/search?query=${keyword}`)
    router.push(`/search?query=${encodeURIComponent(keyword)}`)
  }

  // Handle Search Button Click
  const handleSearch = () => {
    console.log('Searching for:', searchQuery.value)
    // 예시: router.push(`/search?query=${searchQuery.value}`)
  }

  // Scroll to Top Function
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // Computed properties to determine the class for pagination arrows
  const getPageArrowClass = (direction) => {
    if (direction === 'left') {
      return currentPage.value > 1 ? 'black-button' : 'white-button'
    } else if (direction === 'right') {
      return currentPage.value < totalPages.value ? 'black-button' : 'white-button'
    }
  }
  </script>

  <style scoped>
  /* 전역 Box-Sizing 설정 */
  *, *::before, *::after {
    box-sizing: border-box;
  }

  /* 1. 웹 메인페이지 배경색 */
  .main-page {
    background-color: #F7F7F7;
    font-family: 'Noto Sans KR', sans-serif;
  }

  /* 2. 배너 섹션 중앙 정렬 */
  .banner {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* 3. 카테고리 필터 섹션 */
  .category-filter {
    background-color: #FFFFFF;
    border: 1px solid #707070;
    border-radius: 10px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 17px;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.16);
    width: 100%;
    max-width: 1440px;
    height: 120px;
    margin: 80px 0 0 0;
    box-sizing: border-box;
    position: relative; /* add-category-button 위치 조정을 위한 설정 */
  }

  .category-button {
    width: 83px;
    height: 36px;
    border: 1px solid #707070;
    border-radius: 10px;
    background-color: #FFFFFF;
    color: #000000;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s, color 0.3s;
  }

  .category-button.active {
    background-color: #000000;
    color: #FFFFFF;
  }

  .add-category-button {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: #000000;
    color: #FFFFFF;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    position: absolute; /* add-category-button 위치 조정 */
    bottom: 10px; /* 우측 하단으로 10px */
    right: 10px; /* 우측 하단으로 10px */
  }

  /* Category Popup Styles */
  .category-popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .popup-content {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 10px;
    position: relative;
  }

  .close-popup {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
  }

  .popup-categories {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;
  }

  .popup-category-button {
    padding: 10px 20px;
    border: 1px solid #707070;
    border-radius: 10px;
    background-color: #FFFFFF;
    cursor: pointer;
  }

  /* 4. 메인 게시물 News 섹션 */
  .main-news-section {
    display: flex;
    gap: 30px;
    margin-top: 80px;
    flex-wrap: wrap;
    justify-content: center;
    width: 1440px; /* 너비 고정 */
  }

  .post-cards {
    display: flex;
    gap: 20px; /* 간격 20px으로 조정 */
    flex-wrap: nowrap; /* 줄 바꿈 방지 */
    height: 500px; /* 높이 500px 고정 */
  }

  .post-card {
    /* 기존의 일반 .post-card 너비와 높이 제거 */
    border-radius: 10px;
    border: 1px solid #707070;
    background-color: #FFFFFF;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.16);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .post-card.image-news-card,
  .post-card.ranking-card {
    width: 460px; /* 너비 460px으로 조정 */
    height: 500px; /* 높이 500px 유지 */
    border-radius: 10px; /* 모서리 곡선 유지 */
    overflow: hidden; /* 자식 요소가 넘치지 않도록 마스킹 */
  }

  /* Image News Card */
  .image-news-card .post-image {
    width: 100%;
    height: 320px;
    background-size: cover;
    background-position: center;
    /* border-top-left-radius: 10px;
    border-top-right-radius: 10px; */ /* 이미 부모에서 설정하므로 제거 */
  }

  .image-news-card:hover {
    background-color: #000000;
  }

  .image-news-card:hover .post-date,
  .image-news-card:hover .post-title {
    color: #FFFFFF;
  }

  /* Post Info */
  .post-info {
    padding: 10px 15px;
    position: relative;
    height: 180px; /* 요청 사항 1: 높이를 180px로 설정 */
    display: flex;
    flex-direction: column;
    justify-content: space-between; /* 요소들 간의 공간 분배 */
    background-color: rgba(0, 0, 0, 0); /* 초기 배경색 투명 */
    transition: background-color 0.3s;
  }

  /* Post Title */
  .post-title {
    font-family: Arial, sans-serif;
    font-size: 30px;
    font-weight: normal;
    color: #000000;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* 두 줄까지 표시 */
    -webkit-box-orient: vertical;
    margin: 0; /* 불필요한 마진 제거 */
    align-self: flex-start; /* 좌측 상단에 위치 */
    transition: color 0.3s;
  }

  /* Post Info Bottom: Container for Post Date and Post Meta */
  .post-info-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin: 0; /* 요청 사항 3: 간격 제거 */
  }

  /* Post Date */
  .post-date {
    font-family: Arial, sans-serif;
    font-size: 20px;
    font-weight: normal;
    color: #000000;
    margin: 0; /* 불필요한 마진 제거 */
    transition: color 0.3s;
  }

  /* Post Meta */
  .post-meta {
    display: flex;
    gap: 20px;
    align-items: center;
  }

  /* Like Section */
  .like-section, .view-section {
    display: flex;
    align-items: center;
    gap: 5px; /* 아이콘과 숫자 사이 간격 */
  }

  /* Like Button */
  .like-button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 20px;
    padding: 0;
  }

  .like-button:hover {
    transform: scale(1.2);
  }

  /* View Icon */
  .view-icon {
    font-size: 20px;
  }

  /* Like and View Counts */
  .like-count, .view-count {
    font-size: 20px;
    font-weight: bold;
    color: #000000; /* 기본 색상 */
    transition: color 0.3s;
  }

  .image-news-card:hover .like-count,
  .image-news-card:hover .view-count,
  .news-card:hover .like-count,
  .news-card:hover .view-count {
    color: #FFFFFF; /* 마우스 호버 시 #FFFFFF으로 변경 */
  }

  /* Link Button */
  .link-button {
    background-color: transparent;
    border: none;
    color: #0000EE;
    cursor: pointer;
    text-decoration: underline;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 16px;
  }

  /* Ranking Card */
  .post-card.ranking-card {
    padding: 0; /* padding 제거 */
  }

  .ranking-card .top-list {
    /* 아래 마진 제거 */
    margin-bottom: 0;
  }

  .ranking-card h3 {
    font-size: 30px;
    font-weight: bold;
    color: #000000;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px; /* 상단 마진 20px */
    margin-bottom: 30px; /* 하단 마진 30px */
  }

  .ranking-card .top-list + .top-list {
    margin-top: 0; /* 두 번째 top-list의 상단 마진 제거 */
  }

  .ranking-card ol {
    list-style: decimal inside;
    padding-left: 20px;
  }

  .ranking-card ol li {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 20px;
    font-weight: normal;
    color: #000000;
    margin-bottom: 15px;
    cursor: pointer;
    transition: font-weight 0.3s, text-decoration 0.3s;
  }

  .ranking-card ol li:hover {
    font-weight: bold;
    text-decoration: underline;
  }

  .trophy-icon {
    font-size: 30px;
  }

  /* 6. 서브 게시물 News 섹션 */
  .sub-news-section {
    width: 100%;
    max-width: 1440px;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 40px; /* main-news-section과 sub-news-section 간의 간격 */
  }

  .section-state-buttons {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    align-self: flex-start; /* 좌측 상단에 위치 */
  }

  .state-button {
    width: 100px;
    height: 40px;
    border-radius: 10px;
    background-color: #FFFFFF;
    border: 1px solid #707070;
    color: #000000;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
  }

  .state-button.active {
    background-color: #000000;
    color: #FFFFFF;
  }

  .news-cards {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
  }

  .news-card {
    width: 1440px; /* 너비 1440px 고정 */
    height: 540px;
    border-radius: 10px;
    border: 1px solid #707070;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.16);
    padding: 20px;
    box-sizing: border-box;
    background-color: #FFFFFF;
    transition: background-color 0.3s, color 0.3s;
  }

  .news-card:hover {
    background-color: #000000;
    color: #FFFFFF;
  }

  .news-card .category,
  .news-card .news-title,
  .news-card .news-content,
  .news-card .news-date,
  .news-card .like-count,
  .news-card .view-count {
    transition: color 0.3s;
  }

  /* Category */
  .news-card .category {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 30px;
    font-weight: normal;
    color: #828282;
  }

  .news-card:hover .category {
    color: #FFFFFF;
  }

  /* News Title */
  .news-title {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 60px;
    font-weight: bold;
    color: #000000;
    margin: 10px 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .news-card:hover .news-title {
    color: #FFFFFF;
  }

  /* News Content */
  .news-content {
    /* 너비와 높이를 설정 */
    width: 1304px; /* 임의의 너비 설정 */
    height: 234px; /* 임의의 높이 설정 */
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 32px;
    font-weight: normal;
    color: #000000;
    margin: 10px 0;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* 두 줄까지 표시 */
    -webkit-box-orient: vertical;
  }

  .news-card:hover .news-content {
    color: #FFFFFF;
  }

  /* News Meta */
  .news-meta {
    display: flex;
    align-items: center;
    gap: 40px;
    margin-bottom: 10px;
  }

  .news-meta .news-date {
    color: #828282;
  }

  .news-card:hover .news-meta .news-date {
    color: #FFFFFF;
  }

  /* Like and View Counts */
  .news-meta .like-count,
  .news-meta .view-count {
    font-size: 20px;
    font-weight: bold;
    color: #000000; /* 기본 색상 */
    transition: color 0.3s;
  }

  .news-card:hover .news-meta .like-count,
  .news-card:hover .news-meta .view-count {
    color: #FFFFFF; /* 마우스 호버 시 #FFFFFF으로 변경 */
  }

  /* Like Button */
  .like-button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 20px;
    padding: 0;
  }

  .like-button:hover {
    transform: scale(1.2);
  }

  /* View Icon */
  .view-icon {
    font-size: 20px;
  }

  /* Hash Tags */
  .hash-tags {
    display: flex;
    gap: 20px;
    flex-wrap: wrap; /* 5개 태그가 있을 때 줄 바꿈 가능하도록 설정 */
  }

  .hash-tag {
    width: 150px;
    height: 40px;
    border-radius: 10px;
    background-color: #F7F7F7;
    border: 1px solid #707070;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 22px;
    font-weight: normal;
    color: #000000;
  }

  /* 7. Move to Page Section */
  .move-to-page {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-top: 25px;
  }

  /* Pagination Arrow Buttons */
  .page-arrow {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: 1px solid #000000;
    background-color: #FFFFFF;
    color: #000000;
    font-size: 24px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
  }

  .page-arrow:disabled {
    background-color: #FFFFFF;
    color: #000000;
    cursor: not-allowed;
  }

  /* Pagination Arrow Button States */
  .black-button {
    background-color: #000000;
    color: #FFFFFF;
  }

  .white-button {
    background-color: #FFFFFF;
    color: #000000;
  }

  .page-indicator {
    width: 140px;
    height: 40px;
    border-radius: 20px;
    background-color: #FFFFFF;
    border: 1px solid #707070;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 18px;
    color: #000000;
  }

  /* 8. 푸터(Footer) 섹션 */
  /* 이미 Layout.vue에 의해 포함되므로, 중복 스타일링을 피하기 위해 제거 */
  /* 만약 별도로 스타일을 추가하고 싶다면, Layout.vue에서 스타일을 관리하는 것이 좋습니다. */
  </style>
