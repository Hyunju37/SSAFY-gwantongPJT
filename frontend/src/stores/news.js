// src/stores/news.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useNewsStore = defineStore('news', {
  state: () => ({
    newsItem: null,
    similarNews: [],
    newsData: {
        imageNews: [],
        newsCards: [],
        totalCount: 0,
    },
  }),
  actions: {
    async fetchNewsItem(id) {
      try {
        const response = await axios.get(`/api/news/${id}/`)
        this.newsItem = response.data
      } catch (error) {
        console.error('뉴스 데이터 가져오기 오류:', error)
      }
    },
    async fetchSimilarNews(id) {
      try {
        const response = await axios.get(`/api/news/${id}/similar/`)
        this.similarNews = response.data
      } catch (error) {
        console.error('유사한 뉴스 가져오기 오류:', error)
      }
    },
    async searchNews(query) {
        try {
          const response = await axios.get(`/api/news/search/?query=${query}`)
          this.searchResults = response.data
        } catch (error) {
          console.error('검색 결과 가져오기 오류:', error)
        }
    },
        // 카테고리별 뉴스 데이터 가져오기
    async fetchNewsByCategory(category, page) {
      try {
        // 실제 API 호출로 대체
        // const response = await axios.get(`/api/news?category=${category}&page=${page}`)
        // 임의의 데이터 반환
        const response = {
          data: {
            imageNews: [
              // 이미지 뉴스 데이터
            ],
            newsCards: [
              // 뉴스 카드 데이터
            ],
            totalCount: 605, // 총 뉴스 개수
          },
        }
        this.newsData = response.data
        return this.newsData
      } catch (error) {
        console.error('뉴스 데이터 가져오기 오류:', error)
        return {
          imageNews: [],
          newsCards: [],
          totalCount: 0,
        }
      }
    },
    // 카테고리별 뉴스 데이터 가져오기
    async fetchNewsByCategory(category, page) {
        try {
          // 실제 API 호출로 대체
          // const response = await axios.get(`/api/news?category=${category}&page=${page}`)
          // 임의의 데이터 반환
          const response = {
            data: {
              imageNews: [
                // 이미지 뉴스 데이터
              ],
              newsCards: [
                // 뉴스 카드 데이터
              ],
              totalCount: 605, // 총 뉴스 개수
            },
          }
          this.newsData = response.data
          return this.newsData
        } catch (error) {
          console.error('뉴스 데이터 가져오기 오류:', error)
          return {
            imageNews: [],
            newsCards: [],
            totalCount: 0,
          }
        }
      },
  },
})
