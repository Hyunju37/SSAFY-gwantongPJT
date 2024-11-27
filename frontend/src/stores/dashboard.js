// src/store/dashboard.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const useDashboardStore = defineStore('dashboard', () => {
  const API_URL = 'http://127.0.0.1:8000' // 실제 API URL로 변경 필요
  const dataVisualization1 = ref(null)
  const dataVisualization2 = ref(null)
  const dataVisualization3 = ref(null)
  const dataVisualization4 = ref(null)

  const fetchData = async () => {
    try {
      const response1 = await axios.get(`${API_URL}/api/dashboard/data1`)
      dataVisualization1.value = response1.data

      const response2 = await axios.get(`${API_URL}/api/dashboard/data2`)
      dataVisualization2.value = response2.data
      console.log(dataVisualization2.value)

      const response3 = await axios.get(`${API_URL}/api/dashboard/data3`)
      dataVisualization3.value = response3.data

      const response4 = await axios.get(`${API_URL}/api/dashboard/data4`)
      dataVisualization4.value = response4.data
    } catch (error) {
      console.error('데이터 가져오기 실패:', error)
    }
  }

  return { dataVisualization1, dataVisualization2, dataVisualization3, dataVisualization4, fetchData }
})
