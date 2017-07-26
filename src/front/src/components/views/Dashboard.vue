<template>
  <!-- Main content -->
  <section class="content">
    <!-- Info boxes -->
    <div class="row">
          <div class="col-md-6 col-sm-6 col-xs-12">
            <span class="bg-green">上一次检查时间:{{created}}</span>
          </div>
           
    </div>
    <div class="row">
      <div class="col-md-3 col-sm-6 col-xs-12">
        <div class="info-box">
          <span class="info-box-icon bg-aqua">
            <i class="ion ion-android-notifications"></i>
          </span>
  
          <div class="info-box-content">
            <span class="info-box-text">告警</span>
            <span class="info-box-number">{{violation_num}}</span>
          </div>
          <!-- /.info-box-content -->
        </div>
        <!-- /.info-box -->
      </div>
      <!-- /.col -->
      <div class="col-md-3 col-sm-6 col-xs-12">
        <div class="info-box">
          <span class="info-box-icon bg-red">
            <i class="fa ion-android-notifications-none"></i>
          </span>
  
          <div class="info-box-content">
            <span class="info-box-text">新增告警</span>
            <span class="info-box-number">{{violation_num_add}}</span>
          </div>
          <!-- /.info-box-content -->
        </div>
        <!-- /.info-box -->
      </div>
      <!-- /.col -->
  
      <!-- fix for small devices only -->
      <div class="clearfix visible-sm-block"></div>
  
      <div class="col-md-3 col-sm-6 col-xs-12">
        <div class="info-box">
          <span class="info-box-icon bg-aqua">
            <i class="ion ion-document-text"></i>
          </span>
  
          <div class="info-box-content">
            <span class="info-box-text">文件数</span>
            <span class="info-box-number">{{violation_file_num}}</span>
          </div>
          <!-- /.info-box-content -->
        </div>
        <!-- /.info-box -->
      </div>
      <!-- /.col -->
      <div class="col-md-3 col-sm-6 col-xs-12">
        <div class="info-box">
          <span class="info-box-icon bg-yellow">
            <i class="ion ion-document"></i>
          </span>
  
          <div class="info-box-content">
            <span class="info-box-text">新增文件</span>
            <span class="info-box-number">{{violation_file_num_add}}</span>
          </div>
          <!-- /.info-box-content -->
        </div>
        <!-- /.info-box -->
      </div>
      <!-- /.col -->
    </div>
    <!-- /.row -->
  
    <div class="col-xs-12">
      <div class="box">
        <div class="box-header with-border">
          <h3 class="box-title"></h3>
          <div class="box-body">
            <div class="col-sm-12 col-xs-12">
              <p class="text-center">
               <a v-bind:href='report_url'  target="_blank"> <strong>{{job_name}}代码趋势</strong> </a>
              </p>
              <canvas id="trafficBar"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- /.row -->
  
    <!-- Main row -->
    <div class="row">
      <div>
        <vue-good-table :defaultSortBy="{field: 'number', type: 'desc'}" title="" :columns="columns" :rows="rows" :paginate="true" :lineNumbers="true" />
      </div>
    </div>
    <!-- /.row -->
  </section>
  <!-- /.content -->
</template>

<script>
import Chart from 'chart.js'
import axios from 'axios'

export default {
  data () {
    return {
      statistic_url: 'http://192.168.0.88/api/statistics/',
      response: null,
      violation_num: 0,
      violation_num_add: 0,
      violation_file_num: 0,
      violation_file_num_add: 0,
      columns: [
        {
          label: '构建号',
          field: 'number',
          type: 'number',
          html: false
        },
        {
          label: '告警数',
          field: 'violation_num',
          type: 'number'
        },
        {
          label: '新增告警数',
          field: 'violation_num_add',
          type: 'number'
        },
        {
          label: '文件数',
          field: 'violation_file_num',
          type: 'number'
        },
        {
          label: '新文件数',
          field: 'violation_file_num_add',
          type: 'number'
        },

        {
          label: '构建时间',
          field: 'created',
          type: 'date',
          inputFormat: 'YYYY-MM-DD HH:mm:ss',
          outputFormat: 'YYYY-MM-DD HH:mm:ss'
        }
      ],
      rows: [],
      job_name: '',
      report_url: '',
      created: ''
    }
  },
  computed: {},
  mounted () {
    this.$nextTick(() => {
      axios.get(this.statistic_url + this.$route.query.jobId + '/')
        .then(response => {
          if (response.status !== 200) {
            this.error = response.statusText
            return
          }
          this.response = response.data
          this.rows = this.response.rows
          this.violation_num = this.response.violation_num
          this.violation_num_add = this.response.violation_num_add
          this.violation_file_num = this.response.violation_file_num
          this.job_name = this.response.job_name
          this.report_url = this.response.report_url
          this.created = this.response.created
          this.violation_file_num_add = this.response.violation_file_num_add

          var ctx = document.getElementById('trafficBar').getContext('2d')
          var config = {
            type: 'line',
            data: {
              labels: this.response.charts.labels,
              datasets: [{
                label: 'Violation Num',
                fill: false,
                borderColor: '#284184',
                pointBackgroundColor: '#284184',
                backgroundColor: 'rgba(0, 0, 0, 0)',
                data: this.response.charts.violation_nums
              }, {
                label: 'Violation File Num',
                borderColor: '#4BC0C0',
                pointBackgroundColor: '#4BC0C0',
                backgroundColor: 'rgba(0, 0, 0, 0)',
                data: this.response.charts.violation_file_nums
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: !this.isMobile,
              legend: {
                position: 'bottom',
                display: true
              },
              tooltips: {
                mode: 'label',
                xPadding: 10,
                yPadding: 10,
                bodySpacing: 10
              }
            }
          }

          new Chart(ctx, config) // eslint-disable-line no-new
        })
        .catch(error => {
          // Request failed.
          console.log('error', error.response)
          this.error = error.response.statusText
        })
    })
  }
}
</script>
<style>
.info-box {
  cursor: pointer;
}

.info-box-content {
  text-align: center;
  vertical-align: middle;
  display: inherit;
}

.fullCanvas {
  width: 100%;
}
</style>
