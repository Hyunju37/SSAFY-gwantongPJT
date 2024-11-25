// src/stores/news.js
import { defineStore } from 'pinia'
import axios from 'axios'
import defaultImage from '@/assets/default_image.png'

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
        const response = await axios.get(`http://127.0.0.1:8000/api/news/${id}/similar/`)
        this.similarNews = response.data.map(news => ({
          id: news.id,
          title: news.title,
          summary: news.subtitle,
          date: news.write_date || '2024-11-22'
        }))
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
        const response = await axios.get(`http://127.0.0.1:8000/api/news?category=${category}&page=${page}`)

        //console.log(response.data['articles'])
        this.newsData.imageNews = response.data['articles_imageNews'].map(news => ({
          id: news.id,
          title: news.title,
          date: news.write_date || '2024-11-22',
          likes: 10,
          views: 10,
          image: defaultImage
        }))
        this.newsData.newsCards = response.data['articles_newsCards'].map(news => ({
          id: news.id,
          category: category,
          title: news.title,
          content: news.content,
          date: news.write_date || '2024-11-22',
          likes: 10,
          views: 10,
          tags: ['경제', '주식', '시장', '금융', '무역']
        }))
        this.newsData.totalCount = response.data['total_pages']
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
    //
  },
})
