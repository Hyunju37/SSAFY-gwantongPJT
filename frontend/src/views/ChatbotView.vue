<template>
    <Layout>
      <div class="chatbot-page">
        <!-- Main Section -->
        <section class="chatbot-main">
          <!-- Left Side: Similar News Cards -->
          <div class="similar-news">
            <h2>유사한 뉴스</h2>
            <div class="news-cards">
              <div
                class="news-card"
                v-for="card in similarNews"
                :key="card.id"
                @click="navigateToNews(card.id)"
              >
                <!-- 유사도 표시 영역 -->
                <div class="similarity-badge">{{ card.similarity }}</div>
                <!-- 뉴스 제목 -->
                <h3 class="news-title">{{ card.title }}</h3>
                <!-- 뉴스 요약 -->
                <p class="news-summary">{{ card.summary }}</p>
              </div>
            </div>
          </div>
  
          <!-- Right Side: Chat Bot Area -->
          <div class="chatbot-area">
            <h2>Chat Bot</h2>
            <div class="chat-window" ref="chatWindow">
              <div
                v-for="(message, index) in chatbotStore.conversation"
                :key="index"
                :class="['message', message.sender]"
              >
                <span class="message-content">{{ message.content }}</span>
              </div>
              <div v-if="isThinking" class="message bot thinking">
                <span class="message-content">💭 생각 중...</span>
              </div>
            </div>
            <div class="chat-input">
              <input
                v-model="userInput"
                @keyup.enter="sendMessage"
                type="text"
                placeholder="메시지를 입력하세요..."
                class="input-field"
              />
              <button @click="sendMessage" class="send-button">입력</button>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  </template>
  
  <script setup>
  import { ref, onMounted, nextTick } from 'vue'
  import { useChatbotStore } from '@/stores/chatbot' // 필요 시 store 모듈
  import { useRouter } from 'vue-router'
  import Layout from '@/components/Layout.vue'

  const router = useRouter()
  const chatbotStore = useChatbotStore()
  // 상태 변수
  const similarNews = ref([
    {
      id: 1,
      title: '유사 뉴스 1',
      summary: '이것은 유사 뉴스 1의 요약입니다. 이 요약은 길어지면 자동으로 생략됩니다.',
      similarity: '85.50%', // 유사도 데이터 (추후 동적으로 변경)
    },
    {
      id: 2,
      title: '유사 뉴스 2',
      summary: '이것은 유사 뉴스 2의 요약입니다. 이 요약은 길어지면 자동으로 생략됩니다.',
      similarity: '78.25%', // 유사도 데이터 (추후 동적으로 변경)
    },
    {
      id: 3,
      title: '유사 뉴스 3',
      summary: '이것은 유사 뉴스 3의 요약입니다. 이 요약은 길어지면 자동으로 생략됩니다.',
      similarity: '92.10%', // 유사도 데이터 (추후 동적으로 변경)
    },
  ])

  const navigateToNews = (id) => {
    router.push(`/news-posts/${id}`)
  }
  
  // const messages = ref([
  //   { sender: 'bot', content: '안녕하세요! 무엇을 도와드릴까요?' }
  // ])
  
  const userInput = ref('')
  const isThinking = ref(false)

  const chatWindow = ref(null)

  // 메시지 전송 함수
  const sendMessage = async () => {
    const input = userInput.value.trim()
    if (input === '') return
  
    // 사용자 메시지 추가
    chatbotStore.conversation.push({ sender: 'user', content: input })
    userInput.value = ''
  
    // 스크롤을 가장 아래로 이동
    scrollToBottom()
  
    // Bot의 응답을 시뮬레이션
    isThinking.value = true
    await chatbotStore.sendMessage(input)
    isThinking.value = false
    scrollToBottom()
    // setTimeout(() => {
    //   isThinking.value = false
    //   const botResponse = getBotResponse(input)
    //   messages.value.push({ sender: 'bot', content: botResponse })
    //   scrollToBottom()
    // }, 1500) // 1.5초 후에 응답
  }
  
  // Bot 응답 생성 함수 (간단한 예시)
  const getBotResponse = (input) => {
    // 여기서 실제 API 호출이나 로직을 구현할 수 있습니다.
    return `입력하신 "${input}"에 대한 답변입니다.`
  }
  
  // 스크롤 함수
  const scrollToBottom = () => {
    nextTick(() => {
      if (chatWindow.value) {
        chatWindow.value.scrollTop = chatWindow.value.scrollHeight
      }
    })
  }
  
  // 자동 스크롤 초기화
  onMounted(() => {
    scrollToBottom()
  })
  </script>
  
  <style scoped>
  .chatbot-page {
    background-color: #F7F7F7;
    font-family: 'Noto Sans KR', sans-serif;
  }
  
  .chatbot-main {
    display: flex;
    gap: 40px;
    padding: 20px;
    min-height: 1000px; /* 높이를 1800px에서 1000px로 줄임 */
    box-sizing: border-box;
  }
  
  /* 유사한 뉴스 카드 영역 */
  .similar-news {
    flex: 1;
    position: relative;
  }
  
  .similar-news h2 {
    font-size: 28px;
    margin-bottom: 20px;
  }
  
  .news-cards {
    display: flex;
    flex-direction: column;
    gap: 20px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .news-card {
    background-color: #FFFFFF;
    border: 1px solid #707070;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.16);
    position: relative; /* 유사도 배지 위치를 위한 설정 */
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow: hidden; /* 내용이 넘치지 않도록 설정 */
  }
  
  .news-card:hover {
    background-color: #EFEFEF;
  }

  .similarity-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: red;
    color: #FFFFFF;
    padding: 5px 10px;
    border-radius: 50px;
    font-size: 14px;
    font-weight: bold;
  }
  
  .news-title {
    font-size: 20px;
    font-weight: bold;
    color: #000000;
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* 두 줄까지 표시 */
    -webkit-box-orient: vertical;
  }
  
  .news-summary {
    font-size: 16px;
    color: #555555;
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3; /* 세 줄까지 표시 */
    -webkit-box-orient: vertical;
  }
  
  /* Chat Bot 영역 */
  .chatbot-area {
    flex: 2;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .chatbot-area h2 {
    font-size: 28px;
    margin-bottom: 10px;
  }
  
  .chat-window {
    background-color: #FFFFFF;
    border: 1px solid #707070;
    border-radius: 10px;
    padding: 20px;
    flex: 1;
    overflow-y: auto;
    max-height: 600px; /* max-height 조정 */
  }
  
  .message {
    margin-bottom: 15px;
    display: flex;
  }
  
  .message.bot {
    justify-content: flex-start;
  }
  
  .message.user {
    justify-content: flex-end;
  }
  
  .message-content {
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 20px;
    font-size: 16px;
  }
  
  .message.bot .message-content {
    background-color: #EFEFEF;
    color: #000000;
    border-top-left-radius: 0;
  }
  
  .message.user .message-content {
    background-color: #000000;
    color: #FFFFFF;
    border-top-right-radius: 0;
  }
  
  .message.bot.thinking .message-content {
    font-style: italic;
    color: #555555;
  }
  
  .chat-input {
    display: flex;
    gap: 10px;
  }
  
  .input-field {
    flex: 1;
    padding: 10px 15px;
    border: 1px solid #707070;
    border-radius: 20px;
    font-size: 16px;
  }
  
  .send-button {
    padding: 10px 20px;
    border: none;
    background-color: #000000;
    color: #FFFFFF;
    border-radius: 20px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
  }
  
  .send-button:hover {
    background-color: #333333;
  }
  
  /* 반응형 디자인 */
  @media (max-width: 1440px) {
    .chatbot-main {
      gap: 20px;
    }
  
    .similar-news h2,
    .chatbot-area h2 {
      font-size: 24px;
    }
  
    .news-title {
      font-size: 18px;
    }
  
    .news-summary {
      font-size: 14px;
    }
  
    .message-content {
      font-size: 14px;
    }
  
    .input-field {
      font-size: 14px;
    }
  
    .send-button {
      font-size: 14px;
      padding: 8px 16px;
    }
  }
  
  @media (max-width: 768px) {
    .chatbot-main {
      flex-direction: column;
      gap: 30px;
    }
  
    .similar-news,
    .chatbot-area {
      width: 100%;
    }
  
    .news-cards {
      flex-direction: row;
      overflow-x: auto;
    }
  
    .news-card {
      min-width: 250px;
    }
  }
  
  @media (max-width: 480px) {
    .chatbot-main {
      padding: 10px;
    }
  
    .similar-news h2,
    .chatbot-area h2 {
      font-size: 20px;
    }
  
    .news-title {
      font-size: 16px;
    }
  
    .news-summary {
      font-size: 12px;
    }
  
    .message-content {
      font-size: 12px;
    }
  
    .input-field {
      font-size: 14px;
      padding: 8px 12px;
    }
  
    .send-button {
      font-size: 14px;
      padding: 8px 16px;
    }
  }
  </style>
  