import { defineStore } from 'pinia'
import axios from 'axios'

export const useChatbotStore = defineStore('chatbot', {
  state: () => ({
    conversation: [
      { sender: 'bot', content: '안녕하세요! 무엇을 도와드릴까요?' }
    ]
  }),
  actions: {
    // 메시지 보내기 함수
    async sendMessage(message) {
      try {
        // 실제 Chat Bot API 엔드포인트로 변경
        const response = await axios.post('http://127.0.0.1:8000/api/chatbot/send/', { message })
        this.conversation.push({
          sender: 'bot',
          content: response.data
        }
        )
      } catch (error) {
        console.error('Error sending message:', error)
        this.conversation.push({
          sender: 'bot',
          content: '죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다.'
        })
      }
    }
  }
})
