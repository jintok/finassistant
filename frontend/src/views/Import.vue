<template>
  <div class="view">
    <div class="flex flex-between mb-4">
      <h2>Import</h2>
    </div>

    <!-- Import History -->
    <div class="card">
      <div class="card-header">
        <span class="card-title">Import History</span>
        <button class="btn btn-primary" @click="showImportModal = true">+ New Import</button>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Source</th>
            <th>Status</th>
            <th>Positions</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="imp in imports" :key="imp.id">
            <td>{{ formatDate(imp.created_at) }}</td>
            <td>{{ imp.source_type }}</td>
            <td>
              <span :class="getStatusClass(imp.status)">{{ imp.status }}</span>
            </td>
            <td>{{ imp.extracted_positions?.length || 0 }}</td>
            <td>
              <button class="btn btn-secondary btn-sm" @click="viewImport(imp)">View</button>
            </td>
          </tr>
          <tr v-if="imports.length === 0">
            <td colspan="5" class="empty-state">No imports yet</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create Import Modal -->
    <div v-if="showImportModal" class="modal-overlay" @click.self="showImportModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3>Start New Import</h3>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Select Portfolio</label>
            <select v-model="newImport.portfolio_id" class="select">
              <option v-for="p in portfolios" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Source</label>
            <select v-model="newImport.source_type" class="select">
              <option value="雪球">雪球 (Xueqiu)</option>
              <option value="同花顺">同花顺 (Tonghuashun)</option>
              <option value="招商银行">招商银行 (CMB)</option>
              <option value="MANUAL">Manual</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showImportModal = false">Cancel</button>
          <button class="btn btn-primary" @click="startImport">Start Import</button>
        </div>
      </div>
    </div>

    <!-- Review Import Modal -->
    <div v-if="showReviewModal" class="modal-overlay" @click.self="showReviewModal = false">
      <div class="modal" style="max-width: 800px;">
        <div class="modal-header">
          <h3>Review Import</h3>
        </div>
        <div class="modal-body">
          <div v-if="currentImport.extracted_positions?.length" class="mb-4">
            <h4>Extracted Positions</h4>
            <table class="table">
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Quantity</th>
                  <th>Price</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(pos, idx) in currentImport.extracted_positions" :key="idx">
                  <td>{{ pos.asset_symbol }}</td>
                  <td>{{ pos.asset_name || '-' }}</td>
                  <td>{{ pos.asset_type }}</td>
                  <td>{{ pos.quantity }}</td>
                  <td>{{ pos.current_price }}</td>
                  <td>
                    <span :class="getConfidenceClass(pos.confidence)">
                      {{ (pos.confidence * 100).toFixed(0) }}%
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty-state">
            <p>No positions extracted yet. Please upload a screenshot.</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-danger" @click="cancelImport">Cancel</button>
          <button class="btn btn-primary" @click="confirmImport">Confirm Import</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api/portfolio';

export default {
  name: 'Import',
  data() {
    return {
      portfolios: [],
      imports: [],
      showImportModal: false,
      showReviewModal: false,
      newImport: { portfolio_id: '', source_type: '雪球' },
      currentImport: {},
    };
  },
  mounted() {
    this.loadPortfolios();
  },
  methods: {
    async loadPortfolios() {
      try {
        const res = await api.getPortfolios();
        this.portfolios = res.data;
        if (this.portfolios.length > 0) {
          this.newImport.portfolio_id = this.portfolios[0].id;
          this.loadImports(this.portfolios[0].id);
        }
      } catch (e) {
        console.error(e);
      }
    },
    async loadImports(portfolioId) {
      try {
        const res = await api.getImports(portfolioId);
        this.imports = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    async startImport() {
      try {
        await api.startImport(this.newImport.portfolio_id, { 
          source_type: this.newImport.source_type 
        });
        this.showImportModal = false;
        await this.loadImports(this.newImport.portfolio_id);
      } catch (e) {
        console.error(e);
      }
    },
    async viewImport(imp) {
      try {
        const res = await api.getImport(imp.id);
        this.currentImport = res.data;
        this.showReviewModal = true;
      } catch (e) {
        console.error(e);
      }
    },
    async confirmImport() {
      try {
        await api.confirmImport(this.currentImport.id);
        this.showReviewModal = false;
        await this.loadImports(this.newImport.portfolio_id);
      } catch (e) {
        console.error(e);
      }
    },
    async cancelImport() {
      try {
        await api.cancelImport(this.currentImport.id);
        this.showReviewModal = false;
        await this.loadImports(this.newImport.portfolio_id);
      } catch (e) {
        console.error(e);
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    getStatusClass(status) {
      const classes = {
        'PENDING': 'badge badge-warning',
        'ANALYZING': 'badge badge-info',
        'REVIEWING': 'badge badge-info',
        'COMPLETED': 'badge badge-success',
        'REJECTED': 'badge badge-danger',
      };
      return classes[status] || 'badge';
    },
    getConfidenceClass(confidence) {
      if (confidence >= 0.8) return 'text-positive';
      if (confidence >= 0.5) return 'text-warning';
      return 'text-negative';
    },
  },
};
</script>
