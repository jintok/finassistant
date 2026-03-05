<template>
  <div class="view">
    <div class="flex flex-between mb-4">
      <h2>Portfolio</h2>
      <button class="btn btn-primary" @click="showCreateModal = true">+ New Portfolio</button>
    </div>

    <!-- Portfolio List -->
    <div v-if="!selectedPortfolio" class="card">
      <div v-if="portfolios.length === 0" class="empty-state">
        <p>No portfolios yet. Create your first portfolio to get started.</p>
      </div>
      <div v-else class="portfolio-grid">
        <div 
          v-for="portfolio in portfolios" 
          :key="portfolio.id" 
          class="portfolio-card"
          @click="selectPortfolio(portfolio)"
        >
          <h3>{{ portfolio.name }}</h3>
          <p class="text-muted">{{ portfolio.base_currency }}</p>
        </div>
      </div>
    </div>

    <!-- Selected Portfolio Detail -->
    <div v-else>
      <div class="flex flex-between mb-4">
        <button class="btn btn-secondary" @click="selectedPortfolio = null">← Back</button>
        <div>
          <button class="btn btn-secondary" @click="refreshData">Refresh</button>
        </div>
      </div>

      <!-- Summary Stats -->
      <div class="stat-grid" v-if="summary">
        <div class="stat-card">
          <div class="stat-label">Total Value</div>
          <div class="stat-value">{{ formatCurrency(summary.total_market_value) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Total Cost</div>
          <div class="stat-value">{{ formatCurrency(summary.total_cost_basis) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Unrealized Gain</div>
          <div class="stat-value" :class="summary.unrealized_gain >= 0 ? 'positive' : 'negative'">
            {{ formatCurrency(summary.unrealized_gain) }} ({{ summary.unrealized_gain_pct }}%)
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Positions</div>
          <div class="stat-value">{{ summary.position_count }}</div>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid-2 mb-4">
        <div class="card">
          <div class="card-header">
            <span class="card-title">Asset Allocation</span>
          </div>
          <div class="chart-container">
            <Pie :data="allocationChartData" :options="chartOptions" />
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <span class="card-title">Performance</span>
          </div>
          <div class="chart-container">
            <Line :data="performanceChartData" :options="lineChartOptions" />
          </div>
        </div>
      </div>

      <!-- Accounts & Positions -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">Positions</span>
          <button class="btn btn-primary btn-sm" @click="showAddPosition = true">+ Add Position</button>
        </div>
        <table class="table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Name</th>
              <th>Type</th>
              <th>Quantity</th>
              <th>Avg Cost</th>
              <th>Current Price</th>
              <th>Market Value</th>
              <th>Gain/Loss</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pos in allPositions" :key="pos.id">
              <td>{{ pos.asset_symbol }}</td>
              <td>{{ pos.asset_name || '-' }}</td>
              <td><span class="badge badge-info">{{ pos.asset_type }}</span></td>
              <td>{{ formatNumber(pos.quantity) }}</td>
              <td>{{ formatCurrency(pos.avg_cost, pos.trade_currency) }}</td>
              <td>{{ formatCurrency(pos.current_price, pos.trade_currency) }}</td>
              <td>{{ formatCurrency(pos.quantity * pos.current_price * pos.exchange_rate) }}</td>
              <td :class="(pos.quantity * pos.current_price * pos.exchange_rate - pos.quantity * pos.avg_cost * pos.exchange_rate) >= 0 ? 'text-positive' : 'text-negative'">
                {{ formatCurrency(pos.quantity * pos.current_price * pos.exchange_rate - pos.quantity * pos.avg_cost * pos.exchange_rate) }}
              </td>
              <td>
                <button class="btn btn-secondary btn-sm" @click="editPosition(pos)">Edit</button>
              </td>
            </tr>
            <tr v-if="allPositions.length === 0">
              <td colspan="9" class="empty-state">No positions yet</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Portfolio Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3>Create Portfolio</h3>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Name</label>
            <input v-model="newPortfolio.name" class="input" placeholder="My Portfolio" />
          </div>
          <div class="form-group">
            <label class="form-label">Base Currency</label>
            <select v-model="newPortfolio.base_currency" class="select">
              <option value="CNY">CNY - Chinese Yuan</option>
              <option value="USD">USD - US Dollar</option>
              <option value="HKD">HKD - Hong Kong Dollar</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showCreateModal = false">Cancel</button>
          <button class="btn btn-primary" @click="createPortfolio">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Pie, Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  ArcElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import api from '@/api/portfolio';

ChartJS.register(
  ArcElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

export default {
  name: 'Portfolio',
  components: { Pie, Line },
  data() {
    return {
      portfolios: [],
      selectedPortfolio: null,
      summary: null,
      showCreateModal: false,
      showAddPosition: false,
      newPortfolio: { name: '', base_currency: 'CNY' },
      allPositions: [],
      snapshots: [],
    };
  },
  computed: {
    allocationChartData() {
      const byType = {};
      this.allPositions.forEach(pos => {
        const value = pos.quantity * pos.current_price * pos.exchange_rate;
        byType[pos.asset_type] = (byType[pos.asset_type] || 0) + value;
      });
      return {
        labels: Object.keys(byType),
        datasets: [{
          data: Object.values(byType),
          backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
        }]
      };
    },
    performanceChartData() {
      return {
        labels: this.snapshots.map(s => new Date(s.snapshot_date).toLocaleDateString()),
        datasets: [{
          label: 'Total Value',
          data: this.snapshots.map(s => s.total_market_value),
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37, 99, 235, 0.1)',
          fill: true,
        }]
      };
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' }
        }
      };
    },
    lineChartOptions() {
        return {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { beginAtZero: false }
          }
        };
    }
  },
  mounted() {
    this.loadPortfolios();
  },
  methods: {
    async loadPortfolios() {
      try {
        const res = await api.getPortfolios();
        this.portfolios = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    async selectPortfolio(portfolio) {
      this.selectedPortfolio = portfolio;
      await this.loadSummary();
      await this.loadPositions();
      await this.loadSnapshots();
    },
    async loadSummary() {
      try {
        const res = await api.getPortfolioSummary(this.selectedPortfolio.id);
        this.summary = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    async loadPositions() {
      try {
        const res = await api.getPortfolio(this.selectedPortfolio.id);
        this.allPositions = [];
        res.data.accounts.forEach(acc => {
          acc.positions.forEach(pos => {
            this.allPositions.push({ ...pos, account_name: acc.name });
          });
        });
      } catch (e) {
        console.error(e);
      }
    },
    async loadSnapshots() {
      try {
        const res = await api.getSnapshots(this.selectedPortfolio.id);
        this.snapshots = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    async createPortfolio() {
      try {
        await api.createPortfolio(this.newPortfolio);
        this.showCreateModal = false;
        this.newPortfolio = { name: '', base_currency: 'CNY' };
        await this.loadPortfolios();
      } catch (e) {
        console.error(e);
      }
    },
    async refreshData() {
      await this.loadSummary();
      await this.loadPositions();
      await this.loadSnapshots();
    },
    editPosition(pos) {
      // TODO: Implement edit position
      console.log('Edit position', pos);
    },
    formatCurrency(value, currency = 'CNY') {
      if (!value) return '0.00';
      return new Intl.NumberFormat('en-US', { 
        style: 'currency', 
        currency: currency 
      }).format(value);
    },
    formatNumber(value) {
      if (!value) return '0';
      return new Intl.NumberFormat('en-US', { maximumFractionDigits: 4 }).format(value);
    }
  }
};
</script>

<style scoped>
.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.portfolio-card {
  padding: 20px;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.2s ease;
}

.portfolio-card:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-md);
}

.portfolio-card h3 {
  margin-bottom: 4px;
}
</style>
