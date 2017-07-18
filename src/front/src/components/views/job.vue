<template>
  <div>
    <h1 class="text-center"></h1>
    <!--<h4 class="text-center">Github Repos</h4>-->
    <modal :show.sync="showModal" effect="fade" width="400">
      <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">
          <b>{{ modal_title }}</b>
        </h4>
      </div>
      <div slot="modal-body" class="modal-body">
        <div class="bs-example" data-example-id="simple-horizontal-form">
          <div class="form-horizontal">
            <div class="form-group">
              <label for="inputEmail3" class="col-sm-2 control-label">svn</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" placeholder="svn地址" v-model="svn_url">
              </div>
            </div>
            <div class="form-group">
              <label for="inputEmail3" class="col-sm-2 control-label">username</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" placeholder="svn账号" v-model="svn_username">
              </div>
            </div>
            <div class="form-group">
              <label for="inputEmail3" class="col-sm-2 control-label">password</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" placeholder="svn密码" v-model="svn_password">
              </div>
            </div>
            <div class="form-group">
              <label for="inputEmail3" class="col-sm-2 control-label">任务名</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" placeholder="" v-model="name">
              </div>
            </div>
            <div class="form-group">
              <label for="inputEmail3" class="col-sm-2 control-label">通知</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" placeholder="多个邮箱逗号分隔" v-model="recipient">
              </div>
            </div>
            <div class="form-group">
              <label for="inputEmail3" class="col-sm-2 control-label">告警阀值</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" placeholder="" v-model="violation_threshold_num">
              </div>
            </div>
  
          </div>
        </div>
      </div>
      <div slot="modal-footer" class="modal-footer">
        <button type="button" class="btn btn-default" @click="showModal = false">退出</button>
        <button type="button" class="btn btn-success" @click="save_job">保存</button>
      </div>
    </modal>
    <section class="content">
      <div class="row">
        <div class="col-md-2">
          <button type="button" class="btn btn-primary btn-sm" v-on:click="create_job">新建</button>
        </div>
        <div class="col-md-6">
          <form class="form-horizontal">
            <div class="form-group">
              <label for="inputEmail3" class="col-sm-2 control-label">排序</label>
              <div class="col-sm-10">
                <select class="form-control">
                  <option>文件数</option>
                  <option>告警数</option>
                </select>
              </div>
            </div>
          </form>
        </div>
      </div>
      <div class="row">
        <div v-if="error">
          Found an error
        </div>
        <div v-else>
          <div class="col-md-4" v-if="response" v-for="repo in response">
            <div class="box box-widget widget-user">
              <div class="widget-user-header bg-aqua-active text-center">
                <h3 class="widget-user-username center-text" @click="edit_job(repo.id)">
                 {{repo.name }}
                </h3>
              </div>
              <div class="widget-user-image">
                <!--v-bind:src-->
                <img class="img-circle" src="http://www.easyicon.net/api/resizeApi.php?id=1209087&size=72" alt="login Avatar">
              </div>
              <div class="box-footer">
                <div class="row">
                  <div class="col-sm-4 border-right">
                    <div class="description-block">
                      <h5 class="description-header">{{repo.violation_info.violation_num}}</h5>
                      <span class="description-text">告警数</span>
                    </div>
                  </div>
                  <div class="col-sm-4 border-right">
                    <div class="description-block">
                        <i class="fa fa-eye">
                          <router-link :to="{ name: 'Statistics', query: { jobId: repo.id }}">详细</router-link>
                        </i>
                    </div>
                  </div>
                  <div class="col-sm-4">
                    <div class="description-block">
                      <h5 class="description-header">{{repo.violation_info.violation_file_num}}</h5>
                      <span class="description-text">文件数</span>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-sm-12" style="text-align: center">{{repo.violation_info.created}}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- /.modal -->
  </div>
</template>
<script>
import axios from 'axios'
import { modal } from 'vue-strap'

export default {
  name: 'Repository',
  components: { modal },
  data () {
    return {
      job_url: 'http://192.168.0.88/api/jobs/',
      response: null,
      error: null,
      showModal: false,
      modal_title: '',
      jobs: {},
      cur_job_id: null,
      action: 'new',
      name: '',
      svn_url: '',
      svn_username: '',
      svn_password: '',
      recipient: '',
      violation_threshold_num: 0
    }
  },
  methods: {
    callGitHub () {
      axios.get(this.job_url)
        .then(response => {
          console.log('GitHub Response:', response)

          if (response.status !== 200) {
            this.error = response.statusText
            return
          }
          this.response = response.data.results
          for (let job of this.response) {
            this.jobs[job.id] = job
          }
        })
        .catch(error => {
          // Request failed.
          console.log('error', error.response)
          this.error = error.response.statusText
        })
    },
    create_job () {
      this.showModal = true
      this.modal_title = '创建任务'
      this.action = 'new'
      this.name = ''
      this.svn_url = ''
      this.svn_username = ''
      this.svn_password = ''
      this.recipient = ''
      this.violation_threshold_num = 999
    },
    edit_job (jobId) {
      let job = this.jobs[jobId]
      this.name = job.name
      this.svn_url = job.svn_url
      this.svn_username = job.svn_username
      this.svn_password = job.svn_password
      this.recipient = job.recipient
      this.violation_threshold_num = job.violation_threshold_num
      this.modal_title = '编辑任务'
      this.action = 'edit'
      this.showModal = true
      this.cur_job_id = jobId
    },
    save_job () {
      let that = this
      if (this.action === 'new') {
        axios.post(this.job_url, {
          name: this.name,
          svn_url: this.svn_url,
          svn_username: this.svn_username,
          svn_password: this.svn_password,
          recipient: this.recipient,
          violation_threshold_num: this.violation_threshold_num
        })
          .then(function (response) {
            that.callGitHub()
            console.log(response)
          })
          .catch(function (error) {
            console.log(error)
          })
      } else {
        axios.patch(this.job_url + this.cur_job_id + '/', {
          name: this.name,
          svn_url: this.svn_url,
          svn_username: this.svn_username,
          svn_password: this.svn_password,
          recipient: this.recipient,
          violation_threshold_num: this.violation_threshold_num
        })
          .then(function (response) {
            that.callGitHub()
            console.log(response)
          })
          .catch(function (error) {
            console.log(error)
          })
      }
      this.showModal = false
    }
  },
  mounted () {
    this.callGitHub()
  }
}
</script>

<style>

</style>
