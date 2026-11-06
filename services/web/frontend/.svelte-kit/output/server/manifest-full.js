export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["car.jpg","logo.svg","photo_error.jpg","telemetry_system.jpg"]),
	mimeTypes: {".jpg":"image/jpeg",".svg":"image/svg+xml"},
	_: {
		client: {start:"_app/immutable/entry/start.Dexhkdku.js",app:"_app/immutable/entry/app.D7ENg0NT.js",imports:["_app/immutable/entry/start.Dexhkdku.js","_app/immutable/chunks/B8fdvvlZ.js","_app/immutable/chunks/D_a3qmiF.js","_app/immutable/chunks/CA1B741S.js","_app/immutable/entry/app.D7ENg0NT.js","_app/immutable/chunks/D_a3qmiF.js","_app/immutable/chunks/DjTmntQW.js","_app/immutable/chunks/C10nFKEW.js","_app/immutable/chunks/CA1B741S.js","_app/immutable/chunks/D38d51VF.js","_app/immutable/chunks/BvlGhvhy.js","_app/immutable/chunks/BuO8jIKk.js","_app/immutable/chunks/s9esyduY.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js')),
			__memo(() => import('./nodes/3.js')),
			__memo(() => import('./nodes/4.js')),
			__memo(() => import('./nodes/5.js')),
			__memo(() => import('./nodes/6.js')),
			__memo(() => import('./nodes/7.js')),
			__memo(() => import('./nodes/8.js')),
			__memo(() => import('./nodes/9.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 4 },
				endpoint: null
			},
			{
				id: "/live/camera",
				pattern: /^\/live\/camera\/?$/,
				params: [],
				page: { layouts: [0,2,], errors: [1,,], leaf: 5 },
				endpoint: null
			},
			{
				id: "/live/readings",
				pattern: /^\/live\/readings\/?$/,
				params: [],
				page: { layouts: [0,2,], errors: [1,,], leaf: 6 },
				endpoint: null
			},
			{
				id: "/logs/camera",
				pattern: /^\/logs\/camera\/?$/,
				params: [],
				page: { layouts: [0,3,], errors: [1,,], leaf: 7 },
				endpoint: null
			},
			{
				id: "/logs/readings",
				pattern: /^\/logs\/readings\/?$/,
				params: [],
				page: { layouts: [0,3,], errors: [1,,], leaf: 8 },
				endpoint: null
			},
			{
				id: "/send",
				pattern: /^\/send\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 9 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
