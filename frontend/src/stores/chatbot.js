import { defineStore } from 'pinia'
import axios from 'axios'

export const useChatbotStore = defineStore('chatbot', {
  state: () => ({
    conversation: []
  }),
  actions: {
    // 메시지 보내기 함수
    async sendMessage(message) {
      try {
        // 실제 Chat Bot API 엔드포인트로 변경
        const response = await axios.post('/api/chatbot/send', { message })
        this.conversation.push(response.data)
      } catch (error) {
        console.error('Error sending message:', error)
      }
    }
  }
})
