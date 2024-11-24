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
        const response = await axios.get(`http://127.0.0.1:8000/api/posts/${id}/`)
        this.newsItem = {
          id: response.data.id,
          title: response.data.title,
          subtitle: response.data.subtitle,
          date: response.data.write_date || '2024-11-22',
          content: response.data.content,
          originalUrl: response.data.url
        }
        //console.log(this.newsItem)
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
          const response = await axios.get(`http://127.0.0.1:8000/api/news/search/?query=${query}`)
          this.searchResults = response.data.map(news => ({
            id: news.id,
            title: news.title,
            summary: news.subtitle,
            date: news.write_date || '2024-11-22'
          }))
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
