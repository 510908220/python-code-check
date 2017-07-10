<template>
  <div>
    <h1 class="text-center">检查任务</h1>
    <!--<h4 class="text-center">Github Repos</h4>-->

    <section class="content">
         <div class="row">
        <div class="col-md-2">
          <button type="button" class="btn btn-primary btn-sm">新建</button>
        </div>
        <div class="col-md-4">
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
          <div class="col-md-3" v-if="response" v-for="repo in response" >
            <div class="box box-widget widget-user">
              <div class="widget-user-header bg-aqua-active text-center">
                <h3 class="widget-user-username center-text">{{repo.name }}</h3>
              </div>
              <div class="widget-user-image">
                <img class="img-circle" v-bind:src="repo.owner.avatar_url" alt="repo.owner.login + ' Avatar'">
              </div>
              <div class="box-footer">
                <div class="row">
                  <div class="col-sm-4 border-right">
                    <div class="description-block">
                      <h5 class="description-header">{{repo.stargazers_count}}</h5>
                      <span class="description-text">告警数</span>
                    </div>
                  </div>
                  <div class="col-sm-4 border-right">
                    <div class="description-block">
                      <a v-bind:href="repo.owner.html_url" target="_blank">
                        <button type="button" class="btn btn-default btn-lg">查看</button>
                      </a>
                    </div>
                  </div>
                  <div class="col-sm-4">
                    <div class="description-block">
                      <h5 class="description-header">{{repo.forks_count}}</h5>
                      <span class="description-text">文件数</span>
                    </div>
                  </div>
                </div>
                <div class="row">
                <div class="col-md-4"></div>
                <div class="col-md-4">
                    <div class="btn-group" role="group" aria-label="...">
  <button type="button" class="btn btn-warning btn-sm">编辑</button>
  <button type="button" class="btn btn-danger btn-sm">删除</button>
</div>
                </div>
                <div class="col-md-4"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'Repository',
  data () {
    return {
      githubUrl: 'https://api.github.com/search/repositories?q=language%3Ajavascript&sort=stars',
      response: null,
      error: null
    }
  },
  methods: {
    callGitHub () {
      axios.get(this.githubUrl)
        .then(response => {
          console.log('GitHub Response:', response)

          if (response.status !== 200) {
            this.error = response.statusText
            return
          }

          this.response = response.data.items
        })
        .catch(error => {
          // Request failed.
          console.log('error', error.response)
          this.error = error.response.statusText
        })
    }
  },
  mounted () {
    this.callGitHub()
  }
}
</script>

<style>
</style>
