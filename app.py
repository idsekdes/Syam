import streamlit as st
import pandas as pd

<!doctype html>
<html lang="id" class="h-full">
 <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aplikasi Pencarian Data Penduduk</title>
  <link rel="icon" type="image/png" href="https://res.cloudinary.com/dpr2vc3b0/image/upload/v1767107096/logo_donggala-fix-2025_napiej.png">
  <script src="/_sdk/element_sdk.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <style>
    body {
      box-sizing: border-box;
    }
    
    .gradient-bg {
      background: linear-gradient(135deg, #8B0000 0%, #4a0000 50%, #1a1a1a 100%);
    }
    
    .card-gradient {
      background: linear-gradient(135deg, rgba(139, 0, 0, 0.9) 0%, rgba(74, 0, 0, 0.95) 100%);
    }
    
    .gold-accent {
      color: #FFD700;
    }
    
    .gold-bg {
      background-color: #FFD700;
    }
    
    .gold-border {
      border-color: #FFD700;
    }
    
    .result-card {
      background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(74, 0, 0, 0.9) 100%);
      border: 1px solid rgba(255, 215, 0, 0.3);
      transition: all 0.3s ease;
    }
    
    .result-card:hover {
      border-color: #FFD700;
      transform: translateY(-2px);
      box-shadow: 0 8px 16px rgba(255, 215, 0, 0.2);
    }
    
    .search-input {
      background: rgba(26, 26, 26, 0.8);
      border: 2px solid rgba(255, 215, 0, 0.3);
      color: #FFD700;
      transition: all 0.3s ease;
    }
    
    .search-input:focus {
      outline: none;
      border-color: #FFD700;
      box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
    }
    
    .search-input::placeholder {
      color: rgba(255, 215, 0, 0.5);
    }
    
    .btn-search {
      background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
      color: #1a1a1a;
      font-weight: bold;
      transition: all 0.3s ease;
    }
    
    .btn-search:hover {
      transform: scale(1.05);
      box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
    }
    
    .btn-search:active {
      transform: scale(0.98);
    }
    
    .loader {
      border: 4px solid rgba(255, 215, 0, 0.2);
      border-top: 4px solid #FFD700;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .stats-card {
      background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 215, 0, 0.05) 100%);
      border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    .copy-btn {
      transition: all 0.3s ease;
    }
    
    .copy-btn:hover {
      transform: scale(1.1);
    }
    
    .toast {
      position: fixed;
      top: 20px;
      right: 20px;
      background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
      color: #1a1a1a;
      padding: 16px 24px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
      font-weight: bold;
      z-index: 9999;
      animation: slideIn 0.3s ease-out, slideOut 0.3s ease-in 2.7s;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    @keyframes slideOut {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
    
    .admin-photo {
      object-fit: cover;
      object-position: center 30%;
    }
  </style>
  <style>@view-transition { navigation: auto; }</style>
  <script src="/_sdk/data_sdk.js" type="text/javascript"></script>
 </head>
 <body class="h-full"><!-- Login Screen -->
  <div id="login-screen" class="w-full h-full gradient-bg overflow-auto flex items-center justify-center px-4">
   <div class="card-gradient rounded-2xl p-8 shadow-2xl max-w-md w-full">
    <div class="text-center mb-8"><img src="https://res.cloudinary.com/dpr2vc3b0/image/upload/v1767107096/logo_donggala-fix-2025_napiej.png" alt="Logo Donggala" class="w-24 h-24 mx-auto mb-4 object-contain" onerror="this.src=''; this.alt='Logo tidak dapat dimuat'; this.style.display='none';">
     <h1 class="text-3xl font-bold gold-accent mb-2">Login Admin</h1>
     <p class="text-gray-300">Masukkan password untuk mengakses sistem</p>
    </div>
    <form id="login-form" class="space-y-4">
     <div><label for="password-input" class="block text-gray-300 mb-2 font-medium">Password</label>
      <div class="relative"><input type="password" id="password-input" class="search-input w-full px-4 py-3 pr-12 rounded-xl" placeholder="Masukkan password admin..." required> <button type="button" id="toggle-password" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gold-accent hover:text-white transition-colors text-2xl" title="Tampilkan/Sembunyikan Password"> 👁️ </button>
      </div>
     </div>
     <div id="login-error" class="hidden text-red-400 text-sm text-center bg-red-900 bg-opacity-30 p-3 rounded-lg">
      ❌ Password salah! Silakan coba lagi.
     </div><button type="submit" class="btn-search w-full px-6 py-4 rounded-xl text-lg"> 🔓 Masuk </button>
    </form>
    <div class="mt-6 text-center text-gray-400 text-sm">
     <p>🔒 Akses terbatas untuk admin</p>
    </div>
   </div>
  </div><!-- Main App (Hidden until login) -->
  <div id="app" class="hidden w-full h-full gradient-bg overflow-auto">
   <div class="w-full min-h-full px-4 py-8"><!-- Logout Button -->
    <div class="max-w-6xl mx-auto mb-4 flex justify-end"><button id="logout-button" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-bold transition-all flex items-center gap-2"> 🚪 Keluar </button>
    </div><!-- Header -->
    <div class="max-w-6xl mx-auto mb-8">
     <div class="card-gradient rounded-2xl p-8 shadow-2xl">
      <div class="flex items-center justify-center gap-6 mb-6"><img src="https://res.cloudinary.com/dpr2vc3b0/image/upload/v1767107096/logo_donggala-fix-2025_napiej.png" alt="Logo Donggala" class="w-20 h-20 md:w-24 md:h-24 object-contain" onerror="this.src=''; this.alt='Logo tidak dapat dimuat'; this.style.display='none';">
       <div class="flex-1 text-center">
        <h1 id="app-title" class="text-4xl md:text-5xl font-bold gold-accent mb-3">Sistem Pencarian Data Penduduk</h1>
       </div><img src="https://res.cloudinary.com/di8stbg60/image/upload/v1767107507/SYAM_DIGITAL_ADMIN_dt6quc.jpg" alt="Admin Syam" class="admin-photo w-20 h-20 md:w-24 md:h-24 rounded-full border-4 border-gold-accent shadow-lg" onerror="this.src=''; this.alt='Foto tidak dapat dimuat'; this.style.display='none';">
      </div>
      <p id="app-subtitle" class="text-center text-gray-300 text-lg">Cari dan temukan informasi penduduk dengan mudah dan cepat</p>
     </div>
    </div><!-- Search Section -->
    <div class="max-w-6xl mx-auto mb-8">
     <div class="card-gradient rounded-2xl p-6 shadow-2xl">
      <form id="search-form" class="flex flex-col md:flex-row gap-4">
       <div class="flex-1 relative"><input type="text" id="search-input" class="search-input w-full px-6 py-4 pr-12 rounded-xl text-lg" placeholder="Cari berdasarkan NIK, Nama, Alamat, atau Kecamatan..." autocomplete="off" list="nama-suggestions"> <datalist id="nama-suggestions"> <!-- Options will be populated dynamically --> </datalist> <button type="button" id="clear-search" class="hidden absolute right-3 top-1/2 transform -translate-y-1/2 text-gold-accent hover:text-white transition-colors text-2xl" title="Hapus Pencarian"> ✖️ </button>
       </div><button type="submit" id="search-button" class="btn-search px-8 py-4 rounded-xl text-lg"> 🔍 Cari Data </button>
      </form><!-- Alphabet Filter -->
      <div class="mt-6">
       <h3 class="text-sm font-bold gold-accent mb-3">🔤 Filter berdasarkan huruf awal nama:</h3>
       <div class="flex flex-wrap gap-2" id="alphabet-filter"><button class="alphabet-btn px-3 py-2 rounded-lg text-sm font-bold transition-all bg-gray-800 text-white border border-gold-accent hover:bg-gold-accent hover:text-gray-900" data-letter="ALL"> SEMUA </button> <!-- Alphabet buttons will be generated here -->
       </div>
      </div><!-- Action Buttons -->
      <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4"><button id="export-button" class="btn-search px-6 py-3 rounded-xl text-base flex items-center justify-center gap-2"> 📄 Ekspor Data per Dusun (PDF) </button> <a href="https://docs.google.com/spreadsheets/d/1kUOjlnbZFoXr_LKHUZLeIy_RjURxiQPrDh7UN_0BEvw/edit?usp=sharing" target="_blank" rel="noopener noreferrer" class="btn-search px-6 py-3 rounded-xl text-base flex items-center justify-center gap-2 no-underline"> 📊 Buka Database Penduduk </a>
      </div><!-- Stats -->
      <div id="stats-container" class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4"><!-- Stats will be populated here -->
      </div>
     </div>
    </div><!-- Loading State -->
    <div id="loading" class="hidden max-w-6xl mx-auto">
     <div class="card-gradient rounded-2xl p-12 text-center shadow-2xl">
      <div class="loader mx-auto mb-4"></div>
      <p id="loading-text" class="gold-accent text-xl">Memuat data penduduk...</p>
     </div>
    </div><!-- No Results -->
    <div id="no-results" class="hidden max-w-6xl mx-auto">
     <div class="card-gradient rounded-2xl p-12 text-center shadow-2xl">
      <div class="text-6xl mb-4">
       🔍
      </div>
      <p id="no-results-text" class="gold-accent text-2xl font-bold mb-2">Data Tidak Ditemukan</p>
      <p class="text-gray-300">Coba gunakan kata kunci yang berbeda</p>
     </div>
    </div><!-- Results -->
    <div id="results" class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6"><!-- Results will be populated here -->
    </div><!-- Modal Detail -->
    <div id="modal-overlay" class="hidden fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4">
     <div class="card-gradient rounded-2xl max-w-3xl w-full max-h-[90%] overflow-y-auto shadow-2xl">
      <div class="sticky top-0 card-gradient border-b border-gold-accent p-6 flex justify-between items-center">
       <h2 class="text-2xl font-bold gold-accent">Detail Data Penduduk</h2><button id="close-modal" class="text-white hover:gold-accent text-3xl transition-colors">×</button>
      </div>
      <div id="modal-content" class="p-6"><!-- Modal content will be populated here -->
      </div>
     </div>
    </div><!-- Modal Export Dusun -->
    <div id="export-modal-overlay" class="hidden fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4">
     <div class="card-gradient rounded-2xl max-w-2xl w-full max-h-[90%] overflow-y-auto shadow-2xl">
      <div class="sticky top-0 card-gradient border-b border-gold-accent p-6 flex justify-between items-center">
       <h2 class="text-2xl font-bold gold-accent">📄 Pilih Dusun untuk Ekspor PDF</h2><button id="close-export-modal" class="text-white hover:gold-accent text-3xl transition-colors">×</button>
      </div>
      <div id="export-modal-content" class="p-6">
       <p class="text-gray-300 mb-4">Pilih dusun yang ingin Anda ekspor ke file PDF:</p><!-- Ekspor Semua Button --> <button id="export-all-button" class="w-full mb-6 bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 text-white font-bold py-4 px-6 rounded-xl transition-all flex items-center justify-center gap-3 shadow-lg"> <span class="text-2xl">📚</span> <span class="text-lg">Ekspor SEMUA DUSUN (PDF Gabungan)</span> </button>
       <div class="border-t border-gold-accent pt-4 mb-4">
        <p class="text-gray-400 text-sm text-center">atau pilih dusun tertentu:</p>
       </div>
       <div id="dusun-list" class="space-y-3"><!-- Dusun list will be populated here -->
       </div>
      </div>
     </div>
    </div>
   </div>
  </div>
  <script>
    const defaultConfig = {
      app_title: "Sistem Pencarian Data Penduduk",
      app_subtitle: "Cari dan temukan informasi penduduk dengan mudah dan cepat",
      search_placeholder: "Cari berdasarkan NIK, Nama, Alamat, atau Kecamatan...",
      search_button: "🔍 Cari Data",
      no_results_text: "Data Tidak Ditemukan",
      loading_text: "Memuat data penduduk...",
      background_color: "#8B0000",
      card_color: "#4a0000",
      dark_color: "#1a1a1a",
      gold_color: "#FFD700",
      text_color: "#FFFFFF"
    };

    let allData = [];
    let isLoading = false;
    let currentFilter = 'ALL'; // Track current alphabet filter

    async function onConfigChange(config) {
      document.getElementById('app-title').textContent = config.app_title || defaultConfig.app_title;
      document.getElementById('app-subtitle').textContent = config.app_subtitle || defaultConfig.app_subtitle;
      document.getElementById('search-input').placeholder = config.search_placeholder || defaultConfig.search_placeholder;
      document.getElementById('search-button').innerHTML = config.search_button || defaultConfig.search_button;
      document.getElementById('no-results-text').textContent = config.no_results_text || defaultConfig.no_results_text;
      document.getElementById('loading-text').textContent = config.loading_text || defaultConfig.loading_text;
    }

    function mapToCapabilities(config) {
      return {
        recolorables: [
          {
            get: () => config.background_color || defaultConfig.background_color,
            set: (value) => {
              config.background_color = value;
              window.elementSdk.setConfig({ background_color: value });
            }
          },
          {
            get: () => config.card_color || defaultConfig.card_color,
            set: (value) => {
              config.card_color = value;
              window.elementSdk.setConfig({ card_color: value });
            }
          },
          {
            get: () => config.dark_color || defaultConfig.dark_color,
            set: (value) => {
              config.dark_color = value;
              window.elementSdk.setConfig({ dark_color: value });
            }
          },
          {
            get: () => config.gold_color || defaultConfig.gold_color,
            set: (value) => {
              config.gold_color = value;
              window.elementSdk.setConfig({ gold_color: value });
            }
          },
          {
            get: () => config.text_color || defaultConfig.text_color,
            set: (value) => {
              config.text_color = value;
              window.elementSdk.setConfig({ text_color: value });
            }
          }
        ],
        borderables: [],
        fontEditable: undefined,
        fontSizeable: undefined
      };
    }

    function mapToEditPanelValues(config) {
      return new Map([
        ["app_title", config.app_title || defaultConfig.app_title],
        ["app_subtitle", config.app_subtitle || defaultConfig.app_subtitle],
        ["search_placeholder", config.search_placeholder || defaultConfig.search_placeholder],
        ["search_button", config.search_button || defaultConfig.search_button],
        ["no_results_text", config.no_results_text || defaultConfig.no_results_text],
        ["loading_text", config.loading_text || defaultConfig.loading_text]
      ]);
    }

    function parseCSV(text) {
      const lines = text.split(/\r?\n/);
      const result = [];
      
      if (lines.length === 0) return result;
      
      // Parse header - handle quoted headers
      const headerLine = lines[0];
      const headers = [];
      let currentHeader = '';
      let insideQuotes = false;
      
      for (let i = 0; i < headerLine.length; i++) {
        const char = headerLine[i];
        
        if (char === '"') {
          insideQuotes = !insideQuotes;
        } else if (char === ',' && !insideQuotes) {
          headers.push(currentHeader.trim().replace(/^["']|["']$/g, ''));
          currentHeader = '';
        } else {
          currentHeader += char;
        }
      }
      headers.push(currentHeader.trim().replace(/^["']|["']$/g, ''));
      
      // Parse data rows
      for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;
        
        const values = [];
        let currentValue = '';
        let insideQuotes = false;
        
        for (let j = 0; j < line.length; j++) {
          const char = line[j];
          
          if (char === '"') {
            // Check if this is an escaped quote ("")
            if (insideQuotes && j + 1 < line.length && line[j + 1] === '"') {
              currentValue += '"';
              j++; // Skip next quote
            } else {
              insideQuotes = !insideQuotes;
            }
          } else if (char === ',' && !insideQuotes) {
            values.push(currentValue.trim());
            currentValue = '';
          } else {
            currentValue += char;
          }
        }
        
        // Push last value
        values.push(currentValue.trim());
        
        // Only add row if it has valid data
        if (values.length > 0 && values.some(v => v)) {
          const row = {};
          headers.forEach((header, index) => {
            row[header] = values[index] || '';
          });
          
          // Only add if row has at least name or NIK
          if (row.nama || row.nik) {
            result.push(row);
          }
        }
      }
      
      return result;
    }

    async function fetchData() {
      try {
        const sheetUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRd3_sz649R1j66EVGQIzrBZa-fQJTR0IvBXiFXlI7nlFmQgbG__qVa9EUM5JUkalFQUXaT3oPLlv2Y/pub?gid=0&single=true&output=csv';
        const response = await fetch(sheetUrl);
        
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        const csvText = await response.text();
        const data = parseCSV(csvText);
        
        return data;
      } catch (error) {
        try {
          const altUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRd3_sz649R1j66EVGQIzrBZa-fQJTR0IvBXiFXlI7nlFmQgbG__qVa9EUM5JUkalFQUXaT3oPLlv2Y/pub?output=csv';
          const response = await fetch(altUrl);
          const csvText = await response.text();
          const data = parseCSV(csvText);
          return data;
        } catch (fallbackError) {
          return [];
        }
      }
    }
    
    function updateDropdownOptions(letter) {
      const datalist = document.getElementById('nama-suggestions');
      
      // Filter names based on selected letter
      let filteredNames = [];
      if (letter === 'ALL') {
        filteredNames = allData.map(row => row.nama).filter(Boolean);
      } else {
        filteredNames = allData
          .filter(row => {
            const nama = (row.nama || '').trim().toUpperCase();
            return nama.startsWith(letter);
          })
          .map(row => row.nama);
      }
      
      // Remove duplicates and sort
      filteredNames = [...new Set(filteredNames)].sort();
      
      // Update datalist with filtered names
      datalist.innerHTML = filteredNames.map(nama => `<option value="${nama}">`).join('');
    }

    function searchData(query) {
      let filteredData = allData;
      
      // Apply alphabet filter first
      if (currentFilter !== 'ALL') {
        filteredData = filteredData.filter(row => {
          const nama = (row.nama || '').trim().toUpperCase();
          return nama.startsWith(currentFilter);
        });
      }
      
      // Then apply search query if exists
      if (!query.trim()) {
        return filteredData;
      }
      
      const searchTerm = query.toLowerCase().trim();
      
      return filteredData.filter(row => {
        for (const [key, value] of Object.entries(row)) {
          const fieldValue = String(value).toLowerCase().trim();
          if (fieldValue === searchTerm) {
            return true;
          }
        }
        return false;
      });
    }
    
    function generateAlphabetFilter() {
      const alphabetFilterContainer = document.getElementById('alphabet-filter');
      
      // Get unique first letters from all names
      const firstLetters = new Set();
      allData.forEach(row => {
        const nama = (row.nama || '').trim().toUpperCase();
        if (nama) {
          firstLetters.add(nama.charAt(0));
        }
      });
      
      // Convert to sorted array
      const sortedLetters = Array.from(firstLetters).sort();
      
      // Generate buttons for each letter
      const letterButtons = sortedLetters.map(letter => {
        const count = allData.filter(row => {
          const nama = (row.nama || '').trim().toUpperCase();
          return nama.startsWith(letter);
        }).length;
        
        return `
          <button class="alphabet-btn px-3 py-2 rounded-lg text-sm font-bold transition-all bg-gray-800 text-white border border-gold-accent hover:bg-gold-accent hover:text-gray-900" data-letter="${letter}">
            ${letter} <span class="text-xs">(${count})</span>
          </button>
        `;
      }).join('');
      
      // Get the ALL button HTML
      const allButton = alphabetFilterContainer.querySelector('[data-letter="ALL"]');
      const allCount = allData.length;
      allButton.innerHTML = `SEMUA <span class="text-xs">(${allCount})</span>`;
      
      // Append letter buttons after ALL button
      alphabetFilterContainer.innerHTML = allButton.outerHTML + letterButtons;
      
      // Add click event listeners
      document.querySelectorAll('.alphabet-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const letter = btn.getAttribute('data-letter');
          
          // Update active state - reset all buttons to original state
          document.querySelectorAll('.alphabet-btn').forEach(b => {
            b.classList.remove('bg-gold-accent', 'text-gray-900', 'bg-blue-900');
            b.classList.add('bg-gray-800', 'text-white');
            b.style.color = ''; // Clear inline style
          });
          
          // Set active button to blue background with gold text
          btn.classList.remove('bg-gray-800', 'text-white');
          btn.classList.add('bg-blue-900');
          btn.style.color = '#FFD700';
          
          // Update current filter
          currentFilter = letter;
          
          // Update dropdown options based on filter
          updateDropdownOptions(letter);
          
          // Clear search input
          const searchInput = document.getElementById('search-input');
          searchInput.value = '';
          document.getElementById('clear-search').classList.add('hidden');
          
          // Apply filter
          const results = searchData('');
          displayResults(results);
          displayStats(results);
          
          showToast(`Filter: ${letter === 'ALL' ? 'Semua data' : 'Huruf ' + letter}`);
        });
      });
      
      // Set ALL button as active by default
      const allBtn = document.querySelector('[data-letter="ALL"]');
      if (allBtn) {
        allBtn.classList.remove('bg-gray-800', 'text-white');
        allBtn.classList.add('bg-gold-accent', 'text-gray-900');
      }
    }

    function displayStats(data) {
      const statsContainer = document.getElementById('stats-container');
      
      if (data.length === 0) {
        statsContainer.innerHTML = '';
        return;
      }
      
      const totalData = data.length;
      const uniqueDusun = [...new Set(data.map(d => d.dusun))].filter(Boolean).length;
      const lakiLaki = data.filter(d => d['Jenis Kelamin'] === '1' || d['Jenis Kelamin']?.toLowerCase() === 'laki-laki').length;
      const perempuan = data.filter(d => d['Jenis Kelamin'] === '2' || d['Jenis Kelamin']?.toLowerCase() === 'perempuan').length;
      
      statsContainer.innerHTML = `
        <div class="stats-card rounded-xl p-4 text-center">
          <div class="text-3xl font-bold gold-accent">${totalData}</div>
          <div class="text-gray-300 text-sm mt-1">Total Data</div>
        </div>
        <div class="stats-card rounded-xl p-4">
          <div class="text-center mb-2">
            <div class="text-lg font-bold gold-accent">Laki-laki: ${lakiLaki} orang</div>
          </div>
          <div class="text-center">
            <div class="text-lg font-bold gold-accent">Perempuan: ${perempuan} orang</div>
          </div>
        </div>
        <div class="stats-card rounded-xl p-4 text-center">
          <div class="text-3xl font-bold gold-accent">${uniqueDusun}</div>
          <div class="text-gray-300 text-sm mt-1">Dusun</div>
        </div>
      `;
    }

    function showToast(message) {
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.innerHTML = `<span style="font-size: 20px;">✅</span> <span>${message}</span>`;
      document.body.appendChild(toast);
      
      setTimeout(() => {
        toast.remove();
      }, 3000);
    }

    function copyToClipboard(text, button) {
      const fieldName = button.getAttribute('data-field');
      
      navigator.clipboard.writeText(text).then(() => {
        const originalText = button.innerHTML;
        button.innerHTML = '✅';
        button.style.backgroundColor = '#22c55e';
        button.style.color = '#ffffff';
        
        showToast(`${fieldName} berhasil disalin!`);
        
        setTimeout(() => {
          button.innerHTML = originalText;
          button.style.backgroundColor = '';
          button.style.color = '';
        }, 2000);
      }).catch(err => {
        const originalText = button.innerHTML;
        button.innerHTML = '❌';
        
        showToast('Gagal menyalin teks');
        
        setTimeout(() => {
          button.innerHTML = originalText;
        }, 2000);
      });
    }

    function showModal(row) {
      const modalOverlay = document.getElementById('modal-overlay');
      const modalContent = document.getElementById('modal-content');
      
      const nama = row.nama || '-';
      const nik = row.nik || '-';
      const no_kk = row.no_kk || '-';
      const jenisKelamin = row['Jenis Kelamin'] || '-';
      const tempatLahir = row.tempatlahir || '-';
      const tanggalLahir = row.tanggallahir || '-';
      const umur = row.Umur || row.umur || '-';
      const agama = row.agama || '-';
      const dusun = row.dusun || '-';
      const pendidikan = row.pendidikan_kk_id || '-';
      const pekerjaan = row.pekerjaan_id || '-';
      const statusKawin = row.status_kawin || '-';
      const wargaNegara = row.warganegara_id || '-';
      const nikAyah = row['NIK Ayah'] || '-';
      const namaAyah = row['Nama Ayah'] || '-';
      const nikIbu = row['NIK Ibu'] || '-';
      const namaIbu = row['Nama Ibu'] || '-';
      const status = row.status || '-';
      const alamat = row.alamat || '-';
      const suku = row.suku || '-';
      const foto = row.foto || '';
      
      const genderIcon = (jenisKelamin.toLowerCase() === 'perempuan' || jenisKelamin === '2') ? '👩' : '👨';
      
      modalContent.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Left Column: Photo -->
          <div class="md:col-span-1 flex flex-col items-center">
            ${foto ? `
              <img 
                src="${foto}" 
                alt="Foto ${nama}" 
                class="w-full h-auto rounded-lg object-cover border-4 border-gold-accent shadow-lg"
                style="object-position: center 30%; max-height: 400px;"
                onerror="this.style.display='none'; document.getElementById('fallback-icon-${nik}').style.display='flex';"
              />
              <div id="fallback-icon-${nik}" class="hidden w-full h-64 items-center justify-center border-4 border-gold-accent rounded-lg bg-gray-800">
                <span class="text-8xl">${genderIcon}</span>
              </div>
            ` : `
              <div class="w-full h-64 flex items-center justify-center border-4 border-gold-accent rounded-lg bg-gray-800">
                <span class="text-8xl">${genderIcon}</span>
              </div>
            `}
            <div class="mt-4 text-center w-full">
              <h3 class="text-2xl font-bold gold-accent mb-2">${nama}</h3>
              <div class="flex items-center justify-center gap-2">
                <p class="text-gray-400 text-base">NIK: ${nik}</p>
                <button onclick="copyToClipboard('${nik}', this)" data-field="NIK" class="copy-btn text-gold-accent hover:text-white transition-colors text-sm px-2 py-1 rounded border border-gold-accent hover:bg-gold-accent hover:bg-opacity-20" title="Salin NIK">
                  📋
                </button>
              </div>
            </div>
          </div>
          
          <!-- Right Column: Data -->
          <div class="md:col-span-2 space-y-5">
            <!-- Data Identitas -->
            <div>
              <h4 class="text-xl font-bold gold-accent mb-3 border-b-2 border-gold-accent pb-2">📋 Data Identitas</h4>
              <div class="space-y-2">
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Nomor KK:</span>
                  <div class="flex items-center gap-2 ml-4">
                    <span class="text-white text-right break-words text-base">${no_kk}</span>
                    <button onclick="copyToClipboard('${no_kk}', this)" data-field="Nomor KK" class="copy-btn text-gold-accent hover:text-white transition-colors text-sm px-2 py-1 rounded border border-gold-accent hover:bg-gold-accent hover:bg-opacity-20" title="Salin Nomor KK">
                      📋
                    </button>
                  </div>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Jenis Kelamin:</span>
                  <span class="text-white text-right ml-4 text-base">${jenisKelamin}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Tempat Lahir:</span>
                  <span class="text-white text-right ml-4 text-base">${tempatLahir}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Tanggal Lahir:</span>
                  <span class="text-white text-right ml-4 text-base">${tanggalLahir}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Umur:</span>
                  <span class="text-white text-right ml-4 text-base">${umur} tahun</span>
                </div>
              </div>
            </div>
            
            <!-- Data Sosial -->
            <div>
              <h4 class="text-xl font-bold gold-accent mb-3 border-b-2 border-gold-accent pb-2">👥 Data Sosial</h4>
              <div class="space-y-2">
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Agama:</span>
                  <span class="text-white text-right ml-4 text-base">${agama}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Status Kawin:</span>
                  <span class="text-white text-right ml-4 text-base">${statusKawin}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Kewarganegaraan:</span>
                  <span class="text-white text-right ml-4 text-base">${wargaNegara}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Suku:</span>
                  <span class="text-white text-right ml-4 text-base">${suku}</span>
                </div>
              </div>
            </div>
            
            <!-- Data Pendidikan & Pekerjaan -->
            <div>
              <h4 class="text-xl font-bold gold-accent mb-3 border-b-2 border-gold-accent pb-2">🎓 Pendidikan & Pekerjaan</h4>
              <div class="space-y-2">
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Pendidikan:</span>
                  <span class="text-white text-right ml-4 text-base">${pendidikan}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Pekerjaan:</span>
                  <span class="text-white text-right ml-4 text-base">${pekerjaan}</span>
                </div>
              </div>
            </div>
            
            <!-- Data Alamat -->
            <div>
              <h4 class="text-xl font-bold gold-accent mb-3 border-b-2 border-gold-accent pb-2">📍 Alamat</h4>
              <div class="space-y-2">
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Alamat Lengkap:</span>
                  <span class="text-white text-right ml-4 break-words text-base">${alamat}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Dusun:</span>
                  <span class="text-white text-right ml-4 text-base">${dusun}</span>
                </div>
              </div>
            </div>
            
            <!-- Data Orang Tua -->
            <div>
              <h4 class="text-xl font-bold gold-accent mb-3 border-b-2 border-gold-accent pb-2">👨‍👩‍👧‍👦 Data Orang Tua</h4>
              <div class="space-y-2">
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Nama Ayah:</span>
                  <span class="text-white text-right ml-4 break-words text-base">${namaAyah}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">NIK Ayah:</span>
                  <span class="text-white text-right ml-4 break-words text-base">${nikAyah}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Nama Ibu:</span>
                  <span class="text-white text-right ml-4 break-words text-base">${namaIbu}</span>
                </div>
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">NIK Ibu:</span>
                  <span class="text-white text-right ml-4 break-words text-base">${nikIbu}</span>
                </div>
              </div>
            </div>
            
            <!-- Status -->
            <div>
              <h4 class="text-xl font-bold gold-accent mb-3 border-b-2 border-gold-accent pb-2">✅ Status</h4>
              <div class="space-y-2">
                <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                  <span class="text-gray-400 font-medium text-base">Status:</span>
                  <span class="text-white text-right ml-4 text-base">${status}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- WhatsApp Share Button -->
        <div class="mt-6 pt-6 border-t-2 border-gold-accent">
          <button 
            onclick="shareToWhatsApp('${nik.replace(/'/g, "\\'")}', '${nama.replace(/'/g, "\\'")}', '${no_kk.replace(/'/g, "\\'")}', '${jenisKelamin.replace(/'/g, "\\'")}', '${tempatLahir.replace(/'/g, "\\'")}', '${tanggalLahir.replace(/'/g, "\\'")}', '${umur}', '${agama.replace(/'/g, "\\'")}', '${dusun.replace(/'/g, "\\'")}', '${alamat.replace(/'/g, "\\'")}')"
            class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-6 rounded-xl transition-all flex items-center justify-center gap-3 text-lg"
          >
            <span class="text-2xl">📱</span>
            <span>Bagikan ke WhatsApp</span>
          </button>
        </div>
      `;
      
      modalOverlay.classList.remove('hidden');
    }

    function closeModal() {
      const modalOverlay = document.getElementById('modal-overlay');
      modalOverlay.classList.add('hidden');
    }

    function showExportModal() {
      const exportModalOverlay = document.getElementById('export-modal-overlay');
      const dusunList = document.getElementById('dusun-list');
      
      // Get unique dusun names
      const dusunNames = [...new Set(allData.map(d => d.dusun))].filter(Boolean).sort();
      
      if (dusunNames.length === 0) {
        showToast('Tidak ada data dusun untuk diekspor');
        return;
      }
      
      dusunList.innerHTML = dusunNames.map(dusun => {
        const count = allData.filter(d => d.dusun === dusun).length;
        const safeDusun = dusun.replace(/'/g, "\\'");
        return `
          <button 
            class="export-dusun-btn w-full result-card rounded-xl p-4 text-left hover:border-gold-accent transition-all"
            data-dusun="${safeDusun}"
          >
            <div class="flex justify-between items-center">
              <div>
                <h3 class="text-lg font-bold gold-accent">${dusun}</h3>
                <p class="text-gray-400 text-sm">${count} penduduk</p>
              </div>
              <div class="text-2xl">📄</div>
            </div>
          </button>
        `;
      }).join('');
      
      // Add click event listeners to dusun buttons
      document.querySelectorAll('.export-dusun-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const dusun = btn.getAttribute('data-dusun');
          exportDusunToPDF(dusun);
        });
      });
      
      // Add export all button listener
      const exportAllButton = document.getElementById('export-all-button');
      if (exportAllButton) {
        // Remove existing listeners
        const newExportAllButton = exportAllButton.cloneNode(true);
        exportAllButton.parentNode.replaceChild(newExportAllButton, exportAllButton);
        
        // Add new listener
        newExportAllButton.addEventListener('click', () => {
          exportAllDusunToPDF();
        });
      }
      
      exportModalOverlay.classList.remove('hidden');
    }

    function closeExportModal() {
      const exportModalOverlay = document.getElementById('export-modal-overlay');
      exportModalOverlay.classList.add('hidden');
    }

    function shareToWhatsApp(nik, nama, no_kk, jenisKelamin, tempatLahir, tanggalLahir, umur, agama, dusun, alamat) {
      const message = `*DATA PENDUDUK*\n\n` +
        `📋 *Nama:* ${nama}\n` +
        `🆔 *NIK:* ${nik}\n` +
        `👥 *No. KK:* ${no_kk}\n` +
        `👤 *Jenis Kelamin:* ${jenisKelamin}\n` +
        `📅 *Tempat/Tgl Lahir:* ${tempatLahir}, ${tanggalLahir}\n` +
        `🎂 *Umur:* ${umur} tahun\n` +
        `🕌 *Agama:* ${agama}\n` +
        `📍 *Dusun:* ${dusun}\n` +
        `🏠 *Alamat:* ${alamat}\n\n` +
        `_Data dari Sistem Pencarian Data Penduduk_\n\n` +
        `ℹ️ Info selengkapnya: https://syam.digital/dataku`;
      
      const encodedMessage = encodeURIComponent(message);
      const whatsappUrl = `https://wa.me/?text=${encodedMessage}`;
      
      window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
      
      showToast('Membuka WhatsApp...');
    }

    function exportAllDusunToPDF() {
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF('landscape', 'mm', 'a4');
      
      if (allData.length === 0) {
        showToast('Tidak ada data untuk diekspor');
        return;
      }
      
      showToast('Membuat PDF untuk SEMUA DUSUN...');
      
      // Get unique dusun names
      const dusunNames = [...new Set(allData.map(d => d.dusun))].filter(Boolean).sort();
      
      const pageWidth = doc.internal.pageSize.getWidth();
      const pageHeight = doc.internal.pageSize.getHeight();
      const margin = 10;
      const contentWidth = pageWidth - (2 * margin);
      
      let currentPage = 1;
      let isFirstDusun = true;
      
      function drawHeader(pageNum, dusun) {
        // Header
        doc.setFontSize(16);
        doc.setFont(undefined, 'bold');
        doc.text('DATA PENDUDUK - SEMUA DUSUN', pageWidth / 2, 15, { align: 'center' });
        
        doc.setFontSize(12);
        doc.text(`DUSUN: ${dusun.toUpperCase()}`, pageWidth / 2, 22, { align: 'center' });
        
        const dusunData = allData.filter(d => d.dusun === dusun);
        const lakiLaki = dusunData.filter(d => d['Jenis Kelamin'] === '1' || d['Jenis Kelamin']?.toLowerCase() === 'laki-laki').length;
        const perempuan = dusunData.filter(d => d['Jenis Kelamin'] === '2' || d['Jenis Kelamin']?.toLowerCase() === 'perempuan').length;
        
        doc.setFontSize(9);
        doc.setFont(undefined, 'normal');
        doc.text(`Total Dusun Ini: ${dusunData.length} | Laki-laki: ${lakiLaki} | Perempuan: ${perempuan}`, pageWidth / 2, 28, { align: 'center' });
        doc.text(`Dicetak: ${new Date().toLocaleDateString('id-ID', { day: '2-digit', month: 'long', year: 'numeric' })}`, pageWidth / 2, 33, { align: 'center' });
        
        // Page number
        doc.setFontSize(8);
        doc.text(`Halaman ${pageNum}`, pageWidth - margin, pageHeight - 5, { align: 'right' });
      }
      
      function drawTableHeader(startY) {
        const colWidths = [8, 50, 28, 14, 35, 10, 25, 30, 30, 50];
        let x = margin;
        
        doc.setFillColor(139, 0, 0);
        doc.rect(margin, startY, contentWidth, 8, 'F');
        
        doc.setTextColor(255, 215, 0);
        doc.setFontSize(7);
        doc.setFont(undefined, 'bold');
        
        const headers = ['NO', 'NAMA', 'NIK', 'JK', 'TTL', 'UMUR', 'AGAMA', 'PEKERJAAN', 'PENDIDIKAN', 'ALAMAT'];
        
        headers.forEach((header, i) => {
          doc.text(header, x + (colWidths[i] / 2), startY + 5.5, { align: 'center' });
          x += colWidths[i];
        });
        
        doc.setTextColor(0, 0, 0);
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.1);
        doc.rect(margin, startY, contentWidth, 8);
        
        let lineX = margin;
        for (let i = 0; i < colWidths.length - 1; i++) {
          lineX += colWidths[i];
          doc.line(lineX, startY, lineX, startY + 8);
        }
        
        return startY + 8;
      }
      
      // Process each dusun
      dusunNames.forEach((dusun, dusunIndex) => {
        const dusunData = allData.filter(d => d.dusun === dusun);
        
        if (!isFirstDusun) {
          doc.addPage();
          currentPage++;
        }
        isFirstDusun = false;
        
        drawHeader(currentPage, dusun);
        let y = drawTableHeader(38);
        
        const colWidths = [8, 50, 28, 14, 35, 10, 25, 30, 30, 50];
        const rowHeight = 6;
        
        dusunData.forEach((row, index) => {
          if (y > pageHeight - 20) {
            doc.addPage();
            currentPage++;
            drawHeader(currentPage, dusun);
            y = drawTableHeader(38);
          }
          
          const nama = row.nama || '-';
          const nik = row.nik || '-';
          const jenisKelamin = (row['Jenis Kelamin'] === '1' || row['Jenis Kelamin']?.toLowerCase() === 'laki-laki') ? 'L' : 'P';
          const tempatLahir = row.tempatlahir || '-';
          const tanggalLahir = row.tanggallahir || '-';
          const umur = row.Umur || row.umur || '-';
          const agama = row.agama || '-';
          const pekerjaan = row.pekerjaan_id || '-';
          const pendidikan = row.pendidikan_kk_id || '-';
          const alamat = row.alamat || '-';
          
          const ttl = `${tempatLahir}, ${tanggalLahir}`;
          
          doc.setFontSize(6.5);
          doc.setFont(undefined, 'normal');
          
          let x = margin;
          
          // NO
          doc.text(String(index + 1), x + (colWidths[0] / 2), y + 4, { align: 'center' });
          x += colWidths[0];
          
          // NAMA
          const namaLines = doc.splitTextToSize(nama, colWidths[1] - 2);
          doc.text(namaLines[0] || nama, x + 1, y + 4);
          x += colWidths[1];
          
          // NIK
          doc.text(nik, x + 1, y + 4);
          x += colWidths[2];
          
          // JK
          doc.text(jenisKelamin, x + (colWidths[3] / 2), y + 4, { align: 'center' });
          x += colWidths[3];
          
          // TTL
          const ttlLines = doc.splitTextToSize(ttl, colWidths[4] - 2);
          if (ttlLines.length > 1) {
            doc.text(ttlLines[0], x + 1, y + 2.5);
            doc.text(ttlLines[1], x + 1, y + 5);
          } else {
            doc.text(ttlLines[0] || ttl, x + 1, y + 4);
          }
          x += colWidths[4];
          
          // UMUR
          doc.text(String(umur), x + (colWidths[5] / 2), y + 4, { align: 'center' });
          x += colWidths[5];
          
          // AGAMA
          doc.text(agama, x + 1, y + 4);
          x += colWidths[6];
          
          // PEKERJAAN
          const pekerjaanLines = doc.splitTextToSize(pekerjaan, colWidths[7] - 2);
          doc.text(pekerjaanLines[0] || pekerjaan, x + 1, y + 4);
          x += colWidths[7];
          
          // PENDIDIKAN
          const pendidikanLines = doc.splitTextToSize(pendidikan, colWidths[8] - 2);
          doc.text(pendidikanLines[0] || pendidikan, x + 1, y + 4);
          x += colWidths[8];
          
          // ALAMAT
          const alamatLines = doc.splitTextToSize(alamat, colWidths[9] - 2);
          doc.text(alamatLines[0] || alamat, x + 1, y + 4);
          
          // Draw row borders
          doc.setDrawColor(0, 0, 0);
          doc.setLineWidth(0.1);
          doc.rect(margin, y, contentWidth, rowHeight);
          
          let lineX = margin;
          for (let i = 0; i < colWidths.length - 1; i++) {
            lineX += colWidths[i];
            doc.line(lineX, y, lineX, y + rowHeight);
          }
          
          y += rowHeight;
        });
      });
      
      // Add summary page at the end
      doc.addPage();
      currentPage++;
      
      doc.setFontSize(18);
      doc.setFont(undefined, 'bold');
      doc.text('RINGKASAN DATA SEMUA DUSUN', pageWidth / 2, 20, { align: 'center' });
      
      doc.setFontSize(10);
      doc.setFont(undefined, 'normal');
      
      const totalPenduduk = allData.length;
      const totalLakiLaki = allData.filter(d => d['Jenis Kelamin'] === '1' || d['Jenis Kelamin']?.toLowerCase() === 'laki-laki').length;
      const totalPerempuan = allData.filter(d => d['Jenis Kelamin'] === '2' || d['Jenis Kelamin']?.toLowerCase() === 'perempuan').length;
      
      let summaryY = 40;
      
      doc.text(`Total Penduduk: ${totalPenduduk} orang`, margin, summaryY);
      summaryY += 8;
      doc.text(`Laki-laki: ${totalLakiLaki} orang`, margin, summaryY);
      summaryY += 8;
      doc.text(`Perempuan: ${totalPerempuan} orang`, margin, summaryY);
      summaryY += 8;
      doc.text(`Jumlah Dusun: ${dusunNames.length}`, margin, summaryY);
      summaryY += 15;
      
      doc.setFontSize(12);
      doc.setFont(undefined, 'bold');
      doc.text('Rincian per Dusun:', margin, summaryY);
      summaryY += 10;
      
      doc.setFontSize(9);
      doc.setFont(undefined, 'normal');
      
      dusunNames.forEach((dusun, index) => {
        const dusunData = allData.filter(d => d.dusun === dusun);
        const lakiLaki = dusunData.filter(d => d['Jenis Kelamin'] === '1' || d['Jenis Kelamin']?.toLowerCase() === 'laki-laki').length;
        const perempuan = dusunData.filter(d => d['Jenis Kelamin'] === '2' || d['Jenis Kelamin']?.toLowerCase() === 'perempuan').length;
        
        doc.text(`${index + 1}. ${dusun}: ${dusunData.length} orang (L: ${lakiLaki}, P: ${perempuan})`, margin + 5, summaryY);
        summaryY += 6;
        
        if (summaryY > pageHeight - 20) {
          doc.addPage();
          currentPage++;
          summaryY = 20;
        }
      });
      
      doc.setFontSize(8);
      doc.text(`Halaman ${currentPage}`, pageWidth - margin, pageHeight - 5, { align: 'right' });
      
      // Save PDF
      const filename = `Data_Penduduk_SEMUA_DUSUN_${new Date().getTime()}.pdf`;
      doc.save(filename);
      
      closeExportModal();
      showToast(`PDF SEMUA DUSUN berhasil diunduh! Total ${dusunNames.length} dusun.`);
    }

    function exportDusunToPDF(dusun) {
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF('landscape', 'mm', 'a4');
      
      // Filter data by dusun
      const dusunData = allData.filter(d => d.dusun === dusun);
      
      if (dusunData.length === 0) {
        showToast('Tidak ada data untuk dusun ini');
        return;
      }
      
      showToast(`Membuat PDF untuk Dusun ${dusun}...`);
      
      const pageWidth = doc.internal.pageSize.getWidth();
      const pageHeight = doc.internal.pageSize.getHeight();
      const margin = 10;
      const contentWidth = pageWidth - (2 * margin);
      
      let currentPage = 1;
      
      function drawHeader(pageNum) {
        // Header
        doc.setFontSize(16);
        doc.setFont(undefined, 'bold');
        doc.text('DATA PENDUDUK', pageWidth / 2, 15, { align: 'center' });
        
        doc.setFontSize(12);
        doc.text(`DUSUN: ${dusun.toUpperCase()}`, pageWidth / 2, 22, { align: 'center' });
        
        // Statistics
        const lakiLaki = dusunData.filter(d => d['Jenis Kelamin'] === '1' || d['Jenis Kelamin']?.toLowerCase() === 'laki-laki').length;
        const perempuan = dusunData.filter(d => d['Jenis Kelamin'] === '2' || d['Jenis Kelamin']?.toLowerCase() === 'perempuan').length;
        
        doc.setFontSize(9);
        doc.setFont(undefined, 'normal');
        doc.text(`Total: ${dusunData.length} | Laki-laki: ${lakiLaki} | Perempuan: ${perempuan}`, pageWidth / 2, 28, { align: 'center' });
        doc.text(`Dicetak: ${new Date().toLocaleDateString('id-ID', { day: '2-digit', month: 'long', year: 'numeric' })}`, pageWidth / 2, 33, { align: 'center' });
        
        // Page number
        doc.setFontSize(8);
        doc.text(`Halaman ${pageNum}`, pageWidth - margin, pageHeight - 5, { align: 'right' });
      }
      
      function drawTableHeader(startY) {
        const colWidths = [8, 50, 28, 14, 35, 10, 25, 30, 30, 50];
        let x = margin;
        
        doc.setFillColor(139, 0, 0);
        doc.rect(margin, startY, contentWidth, 8, 'F');
        
        doc.setTextColor(255, 215, 0);
        doc.setFontSize(7);
        doc.setFont(undefined, 'bold');
        
        const headers = ['NO', 'NAMA', 'NIK', 'JK', 'TTL', 'UMUR', 'AGAMA', 'PEKERJAAN', 'PENDIDIKAN', 'ALAMAT'];
        
        headers.forEach((header, i) => {
          doc.text(header, x + (colWidths[i] / 2), startY + 5.5, { align: 'center' });
          x += colWidths[i];
        });
        
        doc.setTextColor(0, 0, 0);
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.1);
        doc.rect(margin, startY, contentWidth, 8);
        
        let lineX = margin;
        for (let i = 0; i < colWidths.length - 1; i++) {
          lineX += colWidths[i];
          doc.line(lineX, startY, lineX, startY + 8);
        }
        
        return startY + 8;
      }
      
      drawHeader(currentPage);
      let y = drawTableHeader(38);
      
      const colWidths = [8, 50, 28, 14, 35, 10, 25, 30, 30, 50];
      const rowHeight = 6;
      
      dusunData.forEach((row, index) => {
        if (y > pageHeight - 20) {
          doc.addPage();
          currentPage++;
          drawHeader(currentPage);
          y = drawTableHeader(38);
        }
        
        const nama = row.nama || '-';
        const nik = row.nik || '-';
        const jenisKelamin = (row['Jenis Kelamin'] === '1' || row['Jenis Kelamin']?.toLowerCase() === 'laki-laki') ? 'L' : 'P';
        const tempatLahir = row.tempatlahir || '-';
        const tanggalLahir = row.tanggallahir || '-';
        const umur = row.Umur || row.umur || '-';
        const agama = row.agama || '-';
        const pekerjaan = row.pekerjaan_id || '-';
        const pendidikan = row.pendidikan_kk_id || '-';
        const alamat = row.alamat || '-';
        
        const ttl = `${tempatLahir}, ${tanggalLahir}`;
        
        doc.setFontSize(6.5);
        doc.setFont(undefined, 'normal');
        
        let x = margin;
        
        // NO
        doc.text(String(index + 1), x + (colWidths[0] / 2), y + 4, { align: 'center' });
        x += colWidths[0];
        
        // NAMA
        const namaLines = doc.splitTextToSize(nama, colWidths[1] - 2);
        doc.text(namaLines[0] || nama, x + 1, y + 4);
        x += colWidths[1];
        
        // NIK
        doc.text(nik, x + 1, y + 4);
        x += colWidths[2];
        
        // JK
        doc.text(jenisKelamin, x + (colWidths[3] / 2), y + 4, { align: 'center' });
        x += colWidths[3];
        
        // TTL - Split into two lines if needed
        const ttlLines = doc.splitTextToSize(ttl, colWidths[4] - 2);
        if (ttlLines.length > 1) {
          doc.text(ttlLines[0], x + 1, y + 2.5);
          doc.text(ttlLines[1], x + 1, y + 5);
        } else {
          doc.text(ttlLines[0] || ttl, x + 1, y + 4);
        }
        x += colWidths[4];
        
        // UMUR
        doc.text(String(umur), x + (colWidths[5] / 2), y + 4, { align: 'center' });
        x += colWidths[5];
        
        // AGAMA
        doc.text(agama, x + 1, y + 4);
        x += colWidths[6];
        
        // PEKERJAAN
        const pekerjaanLines = doc.splitTextToSize(pekerjaan, colWidths[7] - 2);
        doc.text(pekerjaanLines[0] || pekerjaan, x + 1, y + 4);
        x += colWidths[7];
        
        // PENDIDIKAN
        const pendidikanLines = doc.splitTextToSize(pendidikan, colWidths[8] - 2);
        doc.text(pendidikanLines[0] || pendidikan, x + 1, y + 4);
        x += colWidths[8];
        
        // ALAMAT
        const alamatLines = doc.splitTextToSize(alamat, colWidths[9] - 2);
        doc.text(alamatLines[0] || alamat, x + 1, y + 4);
        
        // Draw row borders
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.1);
        doc.rect(margin, y, contentWidth, rowHeight);
        
        let lineX = margin;
        for (let i = 0; i < colWidths.length - 1; i++) {
          lineX += colWidths[i];
          doc.line(lineX, y, lineX, y + rowHeight);
        }
        
        y += rowHeight;
      });
      
      // Save PDF
      const filename = `Data_Penduduk_${dusun.replace(/[^a-zA-Z0-9]/g, '_')}_${new Date().getTime()}.pdf`;
      doc.save(filename);
      
      closeExportModal();
      showToast(`PDF berhasil diunduh!`);
    }

    function displayResults(data) {
      const resultsContainer = document.getElementById('results');
      const loadingContainer = document.getElementById('loading');
      const noResultsContainer = document.getElementById('no-results');
      
      loadingContainer.classList.add('hidden');
      
      if (data.length === 0) {
        resultsContainer.innerHTML = '';
        noResultsContainer.classList.remove('hidden');
        return;
      }
      
      noResultsContainer.classList.add('hidden');
      
      resultsContainer.innerHTML = data.map((row, index) => {
        const nama = row.nama || '-';
        const nik = row.nik || '-';
        const jenisKelamin = row['Jenis Kelamin'] || '-';
        const tempatLahir = row.tempatlahir || '-';
        const tanggalLahir = row.tanggallahir || '-';
        const alamat = row.alamat || '-';
        const dusun = row.dusun || '-';
        const foto = row.foto || '';
        
        const genderIcon = (jenisKelamin.toLowerCase() === 'perempuan' || jenisKelamin === '2') ? '👩' : '👨';
        
        return `
          <div class="result-card rounded-xl p-6 shadow-lg cursor-pointer" data-index="${index}">
            <div class="flex items-center gap-3 mb-4">
              ${foto ? `
                <img 
                  src="${foto}" 
                  alt="Foto ${nama}" 
                  class="w-16 h-16 rounded-full object-cover border-2 border-gold-accent"
                  onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                />
                <div class="text-3xl hidden">${genderIcon}</div>
              ` : `
                <div class="text-3xl">${genderIcon}</div>
              `}
              <div class="flex-1">
                <h3 class="text-xl font-bold gold-accent">${nama}</h3>
                <p class="text-gray-400 text-sm">NIK: ${nik}</p>
              </div>
            </div>
            
            <div class="space-y-2">
              <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                <span class="text-gray-400 text-sm font-medium">Tempat/Tgl Lahir:</span>
                <span class="text-white text-sm text-right ml-4 max-w-xs break-words">${tempatLahir}, ${tanggalLahir}</span>
              </div>
              <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                <span class="text-gray-400 text-sm font-medium">Alamat:</span>
                <span class="text-white text-sm text-right ml-4 max-w-xs break-words">${alamat}</span>
              </div>
              <div class="flex justify-between items-start border-b border-gray-700 pb-2">
                <span class="text-gray-400 text-sm font-medium">Dusun:</span>
                <span class="text-white text-sm text-right ml-4">${dusun}</span>
              </div>
            </div>
            
            <div class="mt-4 text-center">
              <span class="text-white text-sm font-bold">👆 Klik untuk lihat detail lengkap</span>
            </div>
          </div>
        `;
      }).join('');
      
      // Add click event listeners to result cards
      document.querySelectorAll('.result-card').forEach((card, index) => {
        card.addEventListener('click', () => {
          showModal(data[index]);
        });
      });
    }

    async function handleSearch(event) {
      event.preventDefault();
      
      if (isLoading) return;
      
      const searchInput = document.getElementById('search-input');
      const query = searchInput.value;
      
      const loadingContainer = document.getElementById('loading');
      const resultsContainer = document.getElementById('results');
      const noResultsContainer = document.getElementById('no-results');
      
      loadingContainer.classList.remove('hidden');
      resultsContainer.innerHTML = '';
      noResultsContainer.classList.add('hidden');
      
      if (allData.length === 0) {
        isLoading = true;
        allData = await fetchData();
        isLoading = false;
      }
      
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const results = searchData(query);
      
      // If search is empty, show all data in list
      if (!query.trim()) {
        displayResults(results);
        displayStats(results);
      }
      // If only one result found from search, show modal directly
      else if (results.length === 1) {
        loadingContainer.classList.add('hidden');
        showModal(results[0]);
        displayStats(results);
      } else {
        // Multiple or no results, show list
        displayResults(results);
        displayStats(results);
      }
    }

    function handleLogin(event) {
      event.preventDefault();
      
      const passwordInput = document.getElementById('password-input');
      const loginError = document.getElementById('login-error');
      const loginScreen = document.getElementById('login-screen');
      const appScreen = document.getElementById('app');
      
      const password = passwordInput.value.trim();
      const correctPassword = '7203192010#';
      
      if (password === correctPassword) {
        // Login successful
        loginError.classList.add('hidden');
        loginScreen.classList.add('hidden');
        appScreen.classList.remove('hidden');
        
        // Store login state
        sessionStorage.setItem('isLoggedIn', 'true');
        
        // Initialize main app
        initializeMainApp();
        
        showToast('Login berhasil! Selamat datang Admin.');
      } else {
        // Login failed
        loginError.classList.remove('hidden');
        passwordInput.value = '';
        passwordInput.focus();
      }
    }
    
    function handleLogout() {
      const loginScreen = document.getElementById('login-screen');
      const appScreen = document.getElementById('app');
      
      // Clear login state
      sessionStorage.removeItem('isLoggedIn');
      
      // Show login screen
      appScreen.classList.add('hidden');
      loginScreen.classList.remove('hidden');
      
      // Clear password input
      document.getElementById('password-input').value = '';
      
      showToast('Anda telah keluar dari sistem.');
    }
    
    async function initializeMainApp() {
      const searchForm = document.getElementById('search-form');
      const searchInput = document.getElementById('search-input');
      const clearSearchBtn = document.getElementById('clear-search');
      
      searchForm.addEventListener('submit', handleSearch);
      
      // Show/hide clear button based on input
      searchInput.addEventListener('input', () => {
        if (searchInput.value.trim()) {
          clearSearchBtn.classList.remove('hidden');
        } else {
          clearSearchBtn.classList.add('hidden');
        }
      });
      
      // Clear search functionality
      clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearSearchBtn.classList.add('hidden');
        searchInput.focus();
        
        // Reset to show all data
        displayResults(allData);
        displayStats(allData);
        
        showToast('Pencarian dihapus');
      });
      
      // Add export button listener
      const exportButton = document.getElementById('export-button');
      exportButton.addEventListener('click', showExportModal);
      
      // Add modal close listeners
      const closeModalBtn = document.getElementById('close-modal');
      const modalOverlay = document.getElementById('modal-overlay');
      
      closeModalBtn.addEventListener('click', closeModal);
      modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
          closeModal();
        }
      });
      
      // Add export modal close listeners
      const closeExportModalBtn = document.getElementById('close-export-modal');
      const exportModalOverlay = document.getElementById('export-modal-overlay');
      
      closeExportModalBtn.addEventListener('click', closeExportModal);
      exportModalOverlay.addEventListener('click', (e) => {
        if (e.target === exportModalOverlay) {
          closeExportModal();
        }
      });
      
      // Load data
      isLoading = true;
      document.getElementById('loading').classList.remove('hidden');
      allData = await fetchData();
      isLoading = false;
      displayResults(allData);
      displayStats(allData);
      
      // Generate alphabet filter buttons
      generateAlphabetFilter();
      
      // Initialize dropdown with all names
      updateDropdownOptions('ALL');
    }

    async function initialize() {
      if (window.elementSdk) {
        window.elementSdk.init({
          defaultConfig,
          onConfigChange,
          mapToCapabilities,
          mapToEditPanelValues
        });
      }
      
      // Check if already logged in
      const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true';
      
      if (isLoggedIn) {
        // Show app directly
        document.getElementById('login-screen').classList.add('hidden');
        document.getElementById('app').classList.remove('hidden');
        initializeMainApp();
      } else {
        // Show login screen
        document.getElementById('login-screen').classList.remove('hidden');
        document.getElementById('app').classList.add('hidden');
      }
      
      // Add login form listener
      const loginForm = document.getElementById('login-form');
      loginForm.addEventListener('submit', handleLogin);
      
      // Add logout button listener
      const logoutButton = document.getElementById('logout-button');
      logoutButton.addEventListener('click', handleLogout);
      
      // Add toggle password visibility
      const togglePassword = document.getElementById('toggle-password');
      const passwordInput = document.getElementById('password-input');
      
      togglePassword.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        togglePassword.textContent = type === 'password' ? '👁️' : '🙈';
      });
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initialize);
    } else {
      initialize();
    }
  </script>
<script>// 1. FUNGSI LOGIN
        async function handleLogin() {
            const password = document.getElementById('passInput').value;
            const res = await fetch('/api/auth', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ password })
            });

            if (res.ok) {
                document.getElementById('login-screen').classList.add('hidden');
                document.getElementById('app').classList.remove('hidden');
                // Langsung panggil fungsi tarik data
                ambilDataSheets();
            } else {
                document.getElementById('errorMsg').classList.remove('hidden');
            }
        }
</script>
 <script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'9b9227fd77d3926c',t:'MTc2NzYwNzUxNi4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>