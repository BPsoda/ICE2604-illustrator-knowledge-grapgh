const projectPath='http://192.168.31.146:5000/search'
    const app = new Vue({
    el:"#app",
	data:{
	isShow:1,
	isRegister:0,
	},
	methods:{
	commit(){
    window.location.href=projectPath;
	}
	}
    })