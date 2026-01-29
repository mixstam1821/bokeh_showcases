import * as p from "core/properties"
import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"
import {div} from "core/dom"

const Turbo256 = ["#30123b","#311542","#32184a","#341b51","#351e58","#36215f","#372566","#38286d","#392b74","#3a2e7b","#3b3181","#3c3488","#3c378e","#3d3a94","#3e3d9a","#3e40a0","#3e43a5","#3f46ab","#3f49b0","#3f4cb5","#3f4fba","#3f52bf","#3f55c4","#3e58c8","#3e5bcc","#3e5ed0","#3d61d4","#3d64d8","#3c68dc","#3c6bdf","#3b6ee2","#3a71e5","#3974e8","#3977eb","#387aed","#377df0","#3680f2","#3583f4","#3486f6","#3389f8","#328cfa","#318ffc","#2f92fd","#2e95fe","#2d98ff","#2c9bff","#2b9eff","#2aa1ff","#2aa4ff","#29a7fe","#28aafe","#28adfd","#28b0fc","#28b2fb","#28b5fa","#28b8f9","#28bbf8","#28bef6","#28c1f5","#29c3f3","#29c6f2","#2ac9f0","#2accee","#2bceec","#2cd1ea","#2dd3e8","#2ed6e6","#2fd8e4","#31dbe1","#32dddf","#34e0dd","#36e2da","#38e4d8","#3ae6d5","#3ce8d2","#3fead0","#41eccd","#44eeca","#46f0c7","#49f1c4","#4cf3c1","#4ff5be","#52f6bb","#55f8b8","#58f9b4","#5bfbb1","#5efcae","#62fdab","#65fea8","#69ffa4","#6cffa1","#70ff9e","#73ff9b","#77ff98","#7aff95","#7eff92","#81ff8f","#85ff8c","#88ff89","#8cff87","#8fff84","#93ff81","#96fe7f","#9afe7c","#9dfd7a","#a1fd77","#a4fc75","#a7fc73","#abfb71","#aefa6f","#b2f96d","#b5f86b","#b8f769","#bcf667","#bff665","#c2f564","#c5f462","#c9f360","#ccf25f","#cff15d","#d2f05c","#d5ef5a","#d9ee59","#dced57","#dfec56","#e2eb55","#e5ea53","#e8e952","#ebe851","#eee750","#f1e64f","#f4e54e","#f7e34d","#f9e24c","#fce14b","#ffe049","#ffdf48","#ffde47","#ffdd46","#ffdb45","#ffda43","#ffd942","#ffd741","#ffd640","#ffd53e","#ffd33d","#ffd23c","#ffd03a","#ffcf39","#ffcd37","#ffcc36","#ffca35","#ffc933","#ffc732","#ffc630","#ffc42f","#ffc32d","#ffc12c","#ffc02a","#ffbe29","#ffbd27","#ffbb26","#ffba24","#ffb823","#ffb621","#ffb520","#ffb31e","#ffb21d","#ffb01b","#ffaf1a","#ffad18","#ffac17","#ffaa15","#ffa914","#ffa712","#ffa611","#ffa40f","#ffa30e","#ffa10c","#ffa00b","#ff9e09","#ff9d08","#ff9b06","#ff9a05","#ff9803","#ff9702","#ff9500"]

const Viridis256 = ["#440154","#440256","#450457","#450559","#46075a","#46085c","#460a5d","#460b5e","#470d60","#470e61","#471063","#471164","#471365","#481467","#481668","#481769","#48186a","#481a6c","#481b6d","#481c6e","#481d6f","#481f70","#482071","#482173","#482374","#482475","#482576","#482677","#482878","#482979","#472a7a","#472c7a","#472d7b","#472e7c","#472f7d","#46307e","#46327e","#46337f","#463480","#453581","#453781","#453882","#443983","#443a83","#443b84","#433d84","#433e85","#423f85","#424086","#424186","#414287","#414487","#404588","#404688","#3f4788","#3f4889","#3e4989","#3e4a89","#3e4c8a","#3d4d8a","#3d4e8a","#3c4f8a","#3c508b","#3b518b","#3b528b","#3a538b","#3a548c","#39558c","#39568c","#38588c","#38598c","#375a8c","#375b8d","#365c8d","#365d8d","#355e8d","#355f8d","#34608d","#34618d","#33628d","#33638d","#32648e","#32658e","#31668e","#31678e","#31688e","#30698e","#306a8e","#2f6b8e","#2f6c8e","#2e6d8e","#2e6e8e","#2e6f8e","#2d708e","#2d718e","#2c718e","#2c728e","#2c738e","#2b748e","#2b758e","#2a768e","#2a778e","#2a788e","#29798e","#297a8e","#297b8e","#287c8e","#287d8e","#277e8e","#277f8e","#27808e","#26818e","#26828e","#26828e","#25838e","#25848e","#25858e","#24868e","#24878e","#23888e","#23898e","#238a8d","#228b8d","#228c8d","#228d8d","#218e8d","#218f8d","#21908d","#21918c","#20928c","#20928c","#20938c","#1f948c","#1f958b","#1f968b","#1f978b","#1f988b","#1f998a","#1f9a8a","#1e9b8a","#1e9c89","#1e9d89","#1f9e89","#1f9f88","#1fa088","#1fa188","#1fa187","#1fa287","#20a386","#20a486","#21a585","#21a685","#22a785","#22a884","#23a983","#24aa83","#25ab82","#25ac82","#26ad81","#27ad81","#28ae80","#29af7f","#2ab07f","#2cb17e","#2db27d","#2eb37c","#2fb47c","#31b57b","#32b67a","#34b679","#35b779","#37b878","#38b977","#3aba76","#3bbb75","#3dbc74","#3fbc73","#40bd72","#42be71","#44bf70","#46c06f","#48c16e","#4ac16d","#4cc26c","#4ec36b","#50c46a","#52c569","#54c568","#56c667","#58c765","#5ac864","#5cc863","#5ec962","#60ca60","#63cb5f","#65cb5e","#67cc5c","#69cd5b","#6ccd5a","#6ece58","#70cf57","#73d056","#75d054","#77d153","#7ad151","#7cd250","#7fd34e","#81d34d","#84d44b","#86d549","#89d548","#8bd646","#8ed645","#90d743","#93d741","#95d840","#98d83e","#9bd93c","#9dd93b","#a0da39","#a2da37","#a5db36","#a8db34","#aadc32","#addc30","#b0dd2f","#b2dd2d","#b5de2b","#b8de29","#bade28","#bddf26","#c0df25","#c2df23","#c5e021","#c8e020","#cae11f","#cde11d","#d0e11c","#d2e21b","#d5e21a","#d8e219","#dae319","#dde318","#dfe318","#e2e418","#e5e419","#e7e419","#eae51a","#ece51b","#efe51c","#f1e51d","#f4e61e","#f6e620","#f8e621","#fbe723","#fde725"]

const Plasma256 = ["#0d0887","#100788","#130789","#16078a","#19068c","#1b068d","#1d068e","#20068f","#220690","#240691","#260591","#280592","#2a0593","#2c0594","#2e0595","#2f0596","#310597","#330597","#350498","#370499","#38049a","#3a049a","#3c049b","#3e049c","#3f049c","#41049d","#43039e","#44039e","#46039f","#48039f","#4903a0","#4b03a1","#4c02a1","#4e02a2","#5002a2","#5102a3","#5302a3","#5502a4","#5601a4","#5801a4","#5901a5","#5b01a5","#5c01a6","#5e01a6","#6001a6","#6100a7","#6300a7","#6400a7","#6600a7","#6700a8","#6900a8","#6a00a8","#6c00a8","#6e00a8","#6f00a8","#7100a8","#7201a8","#7401a8","#7501a8","#7701a8","#7801a8","#7a02a8","#7b02a8","#7d03a8","#7e03a8","#8004a8","#8104a7","#8305a7","#8405a7","#8606a6","#8707a6","#8808a6","#8a09a5","#8b0aa5","#8d0ba5","#8e0ca4","#8f0da4","#910ea3","#920fa3","#9410a2","#9511a1","#9613a1","#9814a0","#99159f","#9a169f","#9c179e","#9d189d","#9e199d","#a01a9c","#a11b9b","#a21d9a","#a31e9a","#a51f99","#a62098","#a72197","#a82296","#aa2395","#ab2494","#ac2694","#ad2793","#ae2892","#b02991","#b12a90","#b22b8f","#b32c8e","#b42e8d","#b52f8c","#b6308b","#b7318a","#b83289","#ba3388","#bb3488","#bc3587","#bd3786","#be3885","#bf3984","#c03a83","#c13b82","#c23c81","#c33d80","#c43e7f","#c5407e","#c6417d","#c7427c","#c8437b","#c9447a","#ca457a","#cb4679","#cc4778","#cc4977","#cd4a76","#ce4b75","#cf4c74","#d04d73","#d14e72","#d24f71","#d35171","#d45270","#d5536f","#d5546e","#d6556d","#d7566c","#d8576b","#d9586a","#da5a6a","#da5b69","#db5c68","#dc5d67","#dd5e66","#de5f65","#de6164","#df6263","#e06363","#e16462","#e26561","#e26660","#e3685f","#e4695e","#e56a5d","#e56b5d","#e66c5c","#e76e5b","#e76f5a","#e87059","#e97158","#e97257","#ea7457","#eb7556","#eb7655","#ec7754","#ed7953","#ed7a52","#ee7b52","#ef7c51","#ef7e50","#f07f4f","#f0804e","#f1814d","#f1834c","#f2844b","#f3854b","#f3864a","#f48849","#f48948","#f58b47","#f58c46","#f68d45","#f68f44","#f79044","#f79143","#f79342","#f89441","#f89540","#f9973f","#f9983e","#f99a3e","#fa9b3d","#fa9c3c","#fa9e3b","#fb9f3a","#fba139","#fba238","#fca338","#fca537","#fca636","#fca835","#fca934","#fdab33","#fdac33","#fdae32","#fdaf31","#fdb130","#fdb22f","#fdb42f","#fdb52e","#feb72d","#feb82c","#feba2c","#febb2b","#febd2a","#febe2a","#fec029","#fdc229","#fdc328","#fdc527","#fdc627","#fdc827","#fdca26","#fdcb26","#fccd25","#fcce25","#fcd025","#fcd225","#fbd324","#fbd524","#fbd724","#fad824","#fada24","#f9dc24","#f9dd25","#f8df25","#f8e125","#f7e225","#f7e425","#f6e626","#f6e826","#f5e926","#f5eb27","#f4ed27","#f3ee27","#f3f027","#f2f227","#f1f426","#f1f525","#f0f724","#f0f921"]

const Inferno256 = ["#000004","#010005","#010106","#010108","#020109","#02020b","#02020d","#03030f","#030312","#040414","#050416","#060518","#06051a","#07061c","#08071e","#090720","#0a0822","#0b0924","#0c0926","#0d0a29","#0e0b2b","#100b2d","#110c2f","#120d31","#130d34","#140e36","#150e38","#160f3b","#180f3d","#19103f","#1a1042","#1c1044","#1d1147","#1e1149","#20114b","#21114e","#221150","#241253","#251255","#271258","#29115a","#2a115c","#2c115f","#2d1161","#2f1163","#311165","#331067","#341069","#36106b","#38106c","#390f6e","#3b0f70","#3d0f71","#3f0f72","#400f74","#420f75","#440f76","#451077","#471078","#491078","#4a1079","#4c117a","#4e117b","#4f127b","#51127c","#52137c","#54137d","#56147d","#57157e","#59157e","#5a167e","#5c167f","#5d177f","#5f187f","#601880","#621980","#641a80","#651a80","#671b80","#681c81","#6a1c81","#6b1d81","#6d1d81","#6e1e81","#701f81","#721f81","#732081","#752181","#762181","#782281","#792282","#7b2382","#7c2382","#7e2482","#802582","#812581","#832681","#842681","#862781","#882781","#892881","#8b2981","#8c2981","#8e2a81","#902a81","#912b81","#932b80","#942c80","#962c80","#982d80","#992d80","#9b2e7f","#9c2e7f","#9e2f7f","#a02f7f","#a1307e","#a3307e","#a5317e","#a6317d","#a8327d","#aa337d","#ab337c","#ad347c","#ae347b","#b0357b","#b2357b","#b3367a","#b5367a","#b73779","#b83779","#ba3878","#bc3978","#bd3977","#bf3a77","#c03a76","#c23b75","#c43c75","#c53c74","#c73d73","#c83e73","#ca3e72","#cc3f71","#cd4071","#cf4070","#d0416f","#d2426f","#d3436e","#d5446d","#d6456c","#d8456c","#d9466b","#db476a","#dc4869","#de4968","#df4a68","#e04c67","#e24d66","#e34e65","#e44f64","#e55064","#e75263","#e85362","#e95462","#ea5661","#eb5760","#ec5860","#ed5a5f","#ee5b5e","#ef5d5e","#f05f5e","#f1605d","#f2625d","#f2645c","#f3655c","#f4675c","#f4695c","#f56b5c","#f66c5c","#f66e5c","#f7705c","#f7725c","#f8745c","#f8765c","#f9785d","#f9795d","#f97b5d","#fa7d5e","#fa7f5e","#fa815f","#fb835f","#fb8560","#fb8761","#fc8961","#fc8a62","#fc8c63","#fc8e64","#fc9065","#fd9266","#fd9467","#fd9668","#fd9869","#fd9a6a","#fd9b6b","#fe9d6c","#fe9f6d","#fea16e","#fea36f","#fea571","#fea772","#fea973","#feaa74","#feac76","#feae77","#feb078","#feb27a","#feb47b","#feb67c","#feb77e","#feb97f","#febb81","#febd82","#febf84","#fec185","#fec287","#fec488","#fec68a","#fec88c","#feca8d","#fecc8f","#fecd90","#fecf92","#fed194","#fed395","#fed597","#fed799","#fed89a","#fdda9c","#fddc9e","#fddea0","#fde0a1","#fde2a3","#fde3a5","#fde5a7","#fde7a9","#fde9aa","#fdebac","#fcecae","#fceeb0","#fcf0b2","#fcf2b4","#fcf4b6","#fcf6b8","#fcf7b9","#fcf9bb","#fcfbbd","#fcfdbf"]

const Cividis256 = ["#00204d","#00204e","#00214f","#002150","#002251","#002251","#002352","#002353","#002354","#002355","#002456","#002457","#002558","#002559","#00265a","#00265b","#00275c","#00275d","#00285e","#00285f","#002961","#002962","#002a63","#002a64","#002b66","#002b67","#002c68","#002c6a","#002d6b","#002d6d","#002e6e","#002e6f","#002f71","#002f72","#003074","#003075","#003177","#003178","#00327a","#00327b","#00337d","#00337e","#003480","#003481","#003583","#003584","#003586","#003687","#003788","#003789","#00388a","#00388b","#003a8c","#003a8d","#003b8e","#003c8f","#003c90","#003d91","#003e91","#003f92","#003f93","#004093","#004194","#004295","#004395","#004496","#004596","#004696","#004797","#004897","#004998","#004a98","#004b98","#004c99","#004d99","#004e99","#004f99","#00509a","#00519a","#00529a","#00539a","#00549a","#00559b","#00569b","#00579b","#00589b","#00599b","#005a9b","#005b9b","#005d9b","#005e9b","#005f9b","#00609b","#00619b","#00629b","#00639b","#00649b","#00659b","#00669b","#00679b","#00689b","#006a9a","#006b9a","#006c9a","#006d9a","#006e9a","#006f99","#007099","#007199","#007299","#007399","#007498","#007598","#007698","#007797","#007897","#007997","#007a96","#007b96","#007c96","#007d95","#007e95","#007f94","#008094","#008193","#008293","#008392","#008492","#008591","#008691","#008790","#00888f","#00898f","#008a8e","#008b8d","#008c8d","#008d8c","#008e8b","#008f8a","#008f8a","#009089","#009188","#009287","#009386","#009485","#009585","#009684","#009783","#009882","#009881","#009980","#009a7f","#009b7e","#009c7d","#009d7c","#009e7b","#009f7a","#00a078","#00a177","#00a276","#00a374","#00a473","#00a572","#00a671","#00a76f","#00a86e","#00a96d","#00aa6b","#00ab6a","#00ac69","#00ad67","#00ae66","#00af64","#00b063","#00b162","#00b260","#00b35f","#00b45d","#00b55c","#00b65a","#00b759","#00b857","#00b956","#00ba54","#00bb53","#00bc51","#00bd50","#00be4e","#00bf4d","#00c04b","#00c14a","#00c248","#00c347","#00c445","#00c544","#00c642","#00c741","#00c83f","#00c93e","#00ca3c","#00cb3b","#00cc39","#00cd38","#00ce36","#00cf35","#00d034","#00d132","#00d231","#00d330","#02d42e","#0bd52d","#12d62c","#18d72b","#1dd829","#21d928","#25da27","#29db26","#2cdc25","#2fdd24","#32de23","#35df22","#38e021","#3ae220","#3de31f","#3fe41e","#42e51d","#44e61d","#46e71c","#49e81b","#4be91b","#4dea1a","#4feb19","#51ec19","#53ed18","#55ee18","#57ef17","#59f017","#5bf117","#5df216","#5ff316","#61f416","#63f516","#65f615","#67f715","#69f815","#6bf915","#6dfa15","#6ffb15","#71fc15","#73fd15","#75fe15","#77ff15"]



export class SurfaceGlobeView extends LayoutDOMView {
  declare model: SurfaceGlobe

  private container_el?: HTMLDivElement
  private canvas?: HTMLCanvasElement
  private ctx?: CanvasRenderingContext2D
  private animation_id?: number
  private tooltip_el?: HTMLDivElement
  private mouse_x: number = 0
  private mouse_y: number = 0
  
  // Drag state
  private is_dragging: boolean = false
  private drag_start_x: number = 0
  private drag_start_y: number = 0
  private drag_start_rotation: number = 0
  private drag_start_tilt: number = 0
  private hover_enabled: boolean = true
  
  // Pan offset for flat projections
  private pan_offset_x: number = 0
  private pan_offset_y: number = 0
  private drag_start_pan_x: number = 0
  private drag_start_pan_y: number = 0

  override get child_models(): LayoutDOM[] {
    return []
  }

  override connect_signals(): void {
    super.connect_signals()
    
    // Re-render when properties change
    this.connect(this.model.properties.projection.change, () => this.render_globe())
    this.connect(this.model.properties.palette.change, () => this.render_globe())
    this.connect(this.model.properties.rotation.change, () => this.render_globe())
    this.connect(this.model.properties.tilt.change, () => this.render_globe())
    this.connect(this.model.properties.zoom.change, () => this.render_globe())
    this.connect(this.model.properties.enable_hover.change, () => {
      this.hover_enabled = this.model.enable_hover
      // Hide tooltip if hover is disabled
      if (!this.hover_enabled && this.tooltip_el) {
        this.tooltip_el.style.display = 'none'
      }
    })
    this.connect(this.model.properties.autorotate.change, () => {
      if (this.model.autorotate && this.model.projection === 'sphere') {
        this.start_animation()
      } else {
        this.stop_animation()
      }
    })
  }

  override render(): void {
    super.render()
    
    const width = this.model.width ?? 800
    const height = this.model.height ?? 800
    
    // Sync hover enabled state
    this.hover_enabled = this.model.enable_hover
    
    // Set cursor based on projection
    const cursor = (this.model.projection === 'sphere' || this.model.projection === 'surface_3d') ? 'grab' : 'move'
    
    this.container_el = div({style: {
      width: `${width}px`,
      height: `${height}px`,
      background: '#0a0a0a',
      position: 'relative',
      cursor: cursor
    }})
    
    this.canvas = document.createElement('canvas')
    this.canvas.width = width
    this.canvas.height = height
    this.container_el.appendChild(this.canvas)
    
    // Create tooltip
    this.tooltip_el = div({style: {
      position: 'absolute',
      background: 'rgba(0, 0, 0, 0.85)',
      color: 'white',
      padding: '8px 12px',
      borderRadius: '6px',
      fontSize: '13px',
      fontFamily: 'monospace',
      pointerEvents: 'none',
      display: 'none',
      zIndex: '1000',
      border: '1px solid rgba(255, 255, 255, 0.3)',
      whiteSpace: 'nowrap'
    }})
    this.container_el.appendChild(this.tooltip_el)
    
    // Mouse down handler - start drag
    this.canvas.onmousedown = (e) => {
      this.is_dragging = true
      this.drag_start_x = e.clientX
      this.drag_start_y = e.clientY
      
      if (this.model.projection === 'sphere' || this.model.projection === 'surface_3d') {
        // Save rotation/tilt for sphere and surface_3d
        this.drag_start_rotation = this.model.rotation
        this.drag_start_tilt = this.model.tilt
        this.container_el!.style.cursor = 'grabbing'
        
        // Stop autorotate when dragging starts
        if (this.model.autorotate) {
          this.model.autorotate = false
        }
      } else {
        // Save pan offset for flat projections
        this.drag_start_pan_x = this.pan_offset_x
        this.drag_start_pan_y = this.pan_offset_y
        this.container_el!.style.cursor = 'move'
      }
    }
    
    // Mouse move handler - handle drag and tooltip
    this.canvas.onmousemove = (e) => {
      const rect = this.canvas!.getBoundingClientRect()
      this.mouse_x = e.clientX - rect.left
      this.mouse_y = e.clientY - rect.top
      
      if (this.is_dragging) {
        const dx = e.clientX - this.drag_start_x
        const dy = e.clientY - this.drag_start_y
        
        if (this.model.projection === 'sphere' || this.model.projection === 'surface_3d') {
          // Rotation for sphere and surface_3d
          const new_rotation = this.drag_start_rotation + dx * 0.5
          this.model.rotation = ((new_rotation % 360) + 360) % 360
          
          // Update tilt
          const new_tilt = this.drag_start_tilt - dy * 0.5
          this.model.tilt = Math.max(-90, Math.min(90, new_tilt))
        } else {
          // Pan for flat projections
          this.pan_offset_x = this.drag_start_pan_x + dx
          this.pan_offset_y = this.drag_start_pan_y + dy
          this.render_globe()
        }
      } else if (this.model.enable_hover) {
        // Only update tooltip if hover is enabled
        this.update_tooltip()
      }
    }
    
    // Mouse up handler - end drag
    this.canvas.onmouseup = () => {
      this.is_dragging = false
      if (this.model.projection === 'sphere' || this.model.projection === 'surface_3d') {
        this.container_el!.style.cursor = 'grab'
      } else {
        this.container_el!.style.cursor = 'move'
      }
    }
    
    // Mouse leave handler
    this.canvas.onmouseleave = () => {
      this.is_dragging = false
      if (this.model.projection === 'sphere' || this.model.projection === 'surface_3d') {
        this.container_el!.style.cursor = 'grab'
      } else {
        this.container_el!.style.cursor = 'move'
      }
      if (this.tooltip_el) {
        this.tooltip_el.style.display = 'none'
      }
    }
    
    // Mouse wheel handler - zoom
    this.canvas.onwheel = (e) => {
      e.preventDefault()
      
      const zoom_speed = 0.1
      const delta = -Math.sign(e.deltaY)
      const new_zoom = this.model.zoom + delta * zoom_speed
      
      // Clamp zoom between 0.5 and 3.0
      this.model.zoom = Math.max(0.5, Math.min(3.0, new_zoom))
    }
    
    this.shadow_el.appendChild(this.container_el)
    
    this.ctx = this.canvas.getContext('2d', { willReadFrequently: true })!
    
    this.render_globe()
    
    if (this.model.autorotate && this.model.projection === 'sphere') {
      this.start_animation()
    }
  }

  private render_globe(): void {
    if (!this.ctx) return
    
    const projection = this.model.projection
    
    if (projection === 'sphere') {
      this.render_sphere()
    } else if (projection === 'mollweide') {
      this.render_mollweide()
    } else if (projection === 'natural_earth') {
      this.render_natural_earth()
    } else if (projection === 'plate_carree') {
      this.render_plate_carree()
    } else if (projection === 'surface_3d') {
      this.render_surface_3d()
    }
  }

  private render_sphere(): void {
    if (!this.ctx) return
    
    const ctx = this.ctx
    const width = this.model.width ?? 800
    const height = this.model.height ?? 800
    
    // Clear
    ctx.fillStyle = '#0a0a0a'
    ctx.fillRect(0, 0, width, height)
    
    const lons = this.model.lons
    const lats = this.model.lats
    const values = this.model.values
    const n_lat = this.model.n_lat
    const n_lon = this.model.n_lon
    
    const angle_rad = -this.model.rotation * Math.PI / 180
    const tilt_rad = this.model.tilt * Math.PI / 180
    const zoom = this.model.zoom
    const scale = (Math.min(width, height) / 2) * 0.85 * zoom
    const cx = width / 2
    const cy = height / 2
    
    const cos_angle = Math.cos(angle_rad)
    const sin_angle = Math.sin(angle_rad)
    const cos_tilt = Math.cos(tilt_rad)
    const sin_tilt = Math.sin(tilt_rad)
    
    // Project points
    const projected: any[] = []
    
    for (let i = 0; i < lons.length; i++) {
      const lat_rad = lats[i] * Math.PI / 180
      const lon_rad = lons[i] * Math.PI / 180
      
      const x = Math.cos(lat_rad) * Math.cos(-lon_rad)
      const y = Math.cos(lat_rad) * Math.sin(-lon_rad)
      const z = Math.sin(lat_rad)
      
      const x_rot = x * cos_angle - y * sin_angle
      const y_rot = x * sin_angle + y * cos_angle
      const y_tilt = y_rot * cos_tilt - z * sin_tilt
      const z_tilt = y_rot * sin_tilt + z * cos_tilt
      
      projected.push({
        x: cx + x_rot * scale,
        y: cy - z_tilt * scale,
        depth: y_tilt,
        visible: y_tilt > -0.15
      })
    }
    
    // Get palette
    const palette = this.get_palette()
    const {vmin, vmax} = this.get_value_range()
    
    // Draw quads
    const quads: any[] = []
    
    for (let i = 0; i < n_lat - 1; i++) {
      for (let j = 0; j < n_lon - 1; j++) {
        const idx0 = i * n_lon + j
        const idx1 = i * n_lon + (j + 1)
        const idx2 = (i + 1) * n_lon + (j + 1)
        const idx3 = (i + 1) * n_lon + j
        
        const p0 = projected[idx0]
        const p1 = projected[idx1]
        const p2 = projected[idx2]
        const p3 = projected[idx3]
        
        if (p0.visible || p1.visible || p2.visible || p3.visible) {
          const avg_value = (values[idx0] + values[idx1] + values[idx2] + values[idx3]) / 4
          const avg_depth = (p0.depth + p1.depth + p2.depth + p3.depth) / 4
          
          const color = this.value_to_color(avg_value, palette, vmin, vmax)
          
          quads.push({
            depth: avg_depth,
            points: [p0, p1, p2, p3],
            color: color
          })
        }
      }
    }
    
    // Sort back to front
    quads.sort((a, b) => a.depth - b.depth)
    
    // Draw
    for (const quad of quads) {
      ctx.fillStyle = quad.color
      ctx.strokeStyle = quad.color
      ctx.lineWidth = 0.5
      
      ctx.beginPath()
      ctx.moveTo(quad.points[0].x, quad.points[0].y)
      ctx.lineTo(quad.points[1].x, quad.points[1].y)
      ctx.lineTo(quad.points[2].x, quad.points[2].y)
      ctx.lineTo(quad.points[3].x, quad.points[3].y)
      ctx.closePath()
      ctx.fill()
      ctx.stroke()
    }
    
    // Draw coastlines
    if (this.model.show_coastlines) {
      this.draw_coastlines_sphere(cos_angle, sin_angle, cos_tilt, sin_tilt, scale, cx, cy)
    }
  }

  private render_mollweide(): void {
    if (!this.ctx) return
    
    const ctx = this.ctx
    const width = this.model.width ?? 800
    const height = this.model.height ?? 800
    
    ctx.fillStyle = '#0a0a0a'
    ctx.fillRect(0, 0, width, height)
    
    const lons = this.model.lons
    const lats = this.model.lats
    const values = this.model.values
    const n_lat = this.model.n_lat
    const n_lon = this.model.n_lon
    const zoom = this.model.zoom
    const rotation = this.model.rotation
    
    const scale = (Math.min(width, height) / 4) * zoom
    const cx = width / 2 + this.pan_offset_x
    const cy = height / 2 + this.pan_offset_y
    
    const projected: any[] = []
    
    for (let i = 0; i < lons.length; i++) {
      // Apply rotation to longitude
      const rotated_lon = lons[i] - rotation
      const {x, y} = this.project_mollweide(rotated_lon, lats[i])
      projected.push({x: cx + x * scale, y: cy - y * scale})
    }
    
    const palette = this.get_palette()
    const {vmin, vmax} = this.get_value_range()
    
    for (let i = 0; i < n_lat - 1; i++) {
      for (let j = 0; j < n_lon - 1; j++) {
        const idx0 = i * n_lon + j
        const idx1 = i * n_lon + (j + 1)
        const idx2 = (i + 1) * n_lon + (j + 1)
        const idx3 = (i + 1) * n_lon + j
        
        const avg_value = (values[idx0] + values[idx1] + values[idx2] + values[idx3]) / 4
        const color = this.value_to_color(avg_value, palette, vmin, vmax)
        
        ctx.fillStyle = color
        ctx.strokeStyle = color
        ctx.lineWidth = 0.5
        
        ctx.beginPath()
        ctx.moveTo(projected[idx0].x, projected[idx0].y)
        ctx.lineTo(projected[idx1].x, projected[idx1].y)
        ctx.lineTo(projected[idx2].x, projected[idx2].y)
        ctx.lineTo(projected[idx3].x, projected[idx3].y)
        ctx.closePath()
        ctx.fill()
        ctx.stroke()
      }
    }
    
    if (this.model.show_coastlines) {
      this.draw_coastlines_map('mollweide', scale, cx, cy, rotation)
    }
  }

  private project_mollweide(lon: number, lat: number): {x: number, y: number} {
    const lambda = lon * Math.PI / 180
    const phi = lat * Math.PI / 180
    
    let theta = phi
    for (let i = 0; i < 10; i++) {
      const dtheta = -(theta + Math.sin(theta) - Math.PI * Math.sin(phi)) / (1 + Math.cos(theta))
      theta += dtheta
      if (Math.abs(dtheta) < 1e-6) break
    }
    
    const x = (2 * Math.sqrt(2) / Math.PI) * lambda * Math.cos(theta / 2)
    const y = Math.sqrt(2) * Math.sin(theta / 2)
    
    return {x, y}
  }

  private project_natural_earth(lon: number, lat: number): {x: number, y: number} {
    const lplam = lon * Math.PI / 180  // longitude in radians
    const lpphi = lat * Math.PI / 180  // latitude in radians
    
    // Natural Earth projection coefficients
    const A0 = 0.8707
    const A1 = -0.131979
    const A2 = -0.013791
    const A3 = 0.003971
    const A4 = -0.001529
    const B0 = 1.007226
    const B1 = 0.015085
    const B2 = -0.044475
    const B3 = 0.028874
    const B4 = -0.005916
    
    const phi2 = lpphi * lpphi
    const phi4 = phi2 * phi2
    
    const x = lplam * (A0 + phi2 * (A1 + phi2 * (A2 + phi4 * phi2 * (A3 + phi2 * A4))))
    const y = lpphi * (B0 + phi2 * (B1 + phi4 * (B2 + B3 * phi2 + B4 * phi4)))
    
    return {x, y}
  }

  private render_natural_earth(): void {
    if (!this.ctx) return
    
    const ctx = this.ctx
    const width = this.model.width ?? 800
    const height = this.model.height ?? 800
    
    ctx.fillStyle = '#0a0a0a'
    ctx.fillRect(0, 0, width, height)
    
    const lons = this.model.lons
    const lats = this.model.lats
    const values = this.model.values
    const n_lat = this.model.n_lat
    const n_lon = this.model.n_lon
    const zoom = this.model.zoom
    const rotation = this.model.rotation
    
    const scale = (Math.min(width, height) / 3.5) * zoom
    const cx = width / 2 + this.pan_offset_x
    const cy = height / 2 + this.pan_offset_y
    
    const projected: any[] = []
    
    for (let i = 0; i < lons.length; i++) {
      // Apply rotation to longitude
      const rotated_lon = lons[i] - rotation
      const {x, y} = this.project_natural_earth(rotated_lon, lats[i])
      projected.push({x: cx + x * scale, y: cy - y * scale})
    }
    
    const palette = this.get_palette()
    const {vmin, vmax} = this.get_value_range()
    
    for (let i = 0; i < n_lat - 1; i++) {
      for (let j = 0; j < n_lon - 1; j++) {
        const idx0 = i * n_lon + j
        const idx1 = i * n_lon + (j + 1)
        const idx2 = (i + 1) * n_lon + (j + 1)
        const idx3 = (i + 1) * n_lon + j
        
        const avg_value = (values[idx0] + values[idx1] + values[idx2] + values[idx3]) / 4
        const color = this.value_to_color(avg_value, palette, vmin, vmax)
        
        ctx.fillStyle = color
        ctx.strokeStyle = color
        ctx.lineWidth = 0.5
        
        ctx.beginPath()
        ctx.moveTo(projected[idx0].x, projected[idx0].y)
        ctx.lineTo(projected[idx1].x, projected[idx1].y)
        ctx.lineTo(projected[idx2].x, projected[idx2].y)
        ctx.lineTo(projected[idx3].x, projected[idx3].y)
        ctx.closePath()
        ctx.fill()
        ctx.stroke()
      }
    }
    
    if (this.model.show_coastlines) {
      this.draw_coastlines_map('natural_earth', scale, cx, cy, rotation)
    }
  }

  private project_plate_carree(lon: number, lat: number): {x: number, y: number} {
    // Simple equirectangular projection
    const x = lon * Math.PI / 180
    const y = lat * Math.PI / 180
    return {x, y}
  }

  private render_plate_carree(): void {
    if (!this.ctx) return
    
    const ctx = this.ctx
    const width = this.model.width ?? 800
    const height = this.model.height ?? 800
    
    ctx.fillStyle = '#0a0a0a'
    ctx.fillRect(0, 0, width, height)
    
    const lons = this.model.lons
    const lats = this.model.lats
    const values = this.model.values
    const n_lat = this.model.n_lat
    const n_lon = this.model.n_lon
    const zoom = this.model.zoom
    const rotation = this.model.rotation
    
    const scale = (Math.min(width, height) / 3.5) * zoom
    const cx = width / 2 + this.pan_offset_x
    const cy = height / 2 + this.pan_offset_y
    
    const projected: any[] = []
    
    for (let i = 0; i < lons.length; i++) {
      // Apply rotation to longitude
      const rotated_lon = lons[i] - rotation
      const {x, y} = this.project_plate_carree(rotated_lon, lats[i])
      projected.push({x: cx + x * scale, y: cy - y * scale})
    }
    
    const palette = this.get_palette()
    const {vmin, vmax} = this.get_value_range()
    
    for (let i = 0; i < n_lat - 1; i++) {
      for (let j = 0; j < n_lon - 1; j++) {
        const idx0 = i * n_lon + j
        const idx1 = i * n_lon + (j + 1)
        const idx2 = (i + 1) * n_lon + (j + 1)
        const idx3 = (i + 1) * n_lon + j
        
        const avg_value = (values[idx0] + values[idx1] + values[idx2] + values[idx3]) / 4
        const color = this.value_to_color(avg_value, palette, vmin, vmax)
        
        ctx.fillStyle = color
        ctx.strokeStyle = color
        ctx.lineWidth = 0.5
        
        ctx.beginPath()
        ctx.moveTo(projected[idx0].x, projected[idx0].y)
        ctx.lineTo(projected[idx1].x, projected[idx1].y)
        ctx.lineTo(projected[idx2].x, projected[idx2].y)
        ctx.lineTo(projected[idx3].x, projected[idx3].y)
        ctx.closePath()
        ctx.fill()
        ctx.stroke()
      }
    }
    
    if (this.model.show_coastlines) {
      this.draw_coastlines_map('plate_carree', scale, cx, cy, rotation)
    }
  }

  private render_surface_3d(): void {
    if (!this.ctx) return
    
    const ctx = this.ctx
    const width = this.model.width ?? 800
    const height = this.model.height ?? 800
    
    ctx.fillStyle = '#0a0a0a'
    ctx.fillRect(0, 0, width, height)
    
    const lons = this.model.lons  // Treat as X values
    const lats = this.model.lats  // Treat as Y values
    const values = this.model.values  // Treat as Z values
    const n_lat = this.model.n_lat
    const n_lon = this.model.n_lon
    
    const elev_rad = this.model.tilt * Math.PI / 180
    const azim_rad = this.model.rotation * Math.PI / 180
    const zoom = this.model.zoom
    
    // Project 3D surface
    const projected: any[] = []
    
    for (let i = 0; i < lons.length; i++) {
      const x = lons[i]
      const y = lats[i]
      const z = values[i]
      
      // Rotate around Z axis (azimuth)
      const x_rot = x * Math.cos(azim_rad) - y * Math.sin(azim_rad)
      const y_rot = x * Math.sin(azim_rad) + y * Math.cos(azim_rad)
      
      // Project to 2D with elevation
      const x_proj = x_rot
      const z_proj = y_rot * Math.sin(elev_rad) + z * Math.cos(elev_rad)
      const depth = y_rot * Math.cos(elev_rad) - z * Math.sin(elev_rad)
      
      projected.push({
        x: x_proj,
        y: z_proj,
        depth: depth
      })
    }
    
    // Find bounds for scaling
    let x_min = Infinity, x_max = -Infinity
    let y_min = Infinity, y_max = -Infinity
    
    for (const p of projected) {
      if (p.x < x_min) x_min = p.x
      if (p.x > x_max) x_max = p.x
      if (p.y < y_min) y_min = p.y
      if (p.y > y_max) y_max = p.y
    }
    
    const x_range = x_max - x_min
    const y_range = y_max - y_min
    const scale = (Math.min(width, height) / Math.max(x_range, y_range)) * 0.7 * zoom
    
    const cx = width / 2
    const cy = height / 2
    
    // Scale and center
    const screen_projected: any[] = []
    for (const p of projected) {
      screen_projected.push({
        x: cx + (p.x - (x_min + x_max) / 2) * scale,
        y: cy - (p.y - (y_min + y_max) / 2) * scale,
        depth: p.depth
      })
    }
    
    const palette = this.get_palette()
    const {vmin, vmax} = this.get_value_range()
    
    // Create and sort quads by depth
    const quads: any[] = []
    
    for (let i = 0; i < n_lat - 1; i++) {
      for (let j = 0; j < n_lon - 1; j++) {
        const idx0 = i * n_lon + j
        const idx1 = i * n_lon + (j + 1)
        const idx2 = (i + 1) * n_lon + (j + 1)
        const idx3 = (i + 1) * n_lon + j
        
        const p0 = screen_projected[idx0]
        const p1 = screen_projected[idx1]
        const p2 = screen_projected[idx2]
        const p3 = screen_projected[idx3]
        
        const avg_value = (values[idx0] + values[idx1] + values[idx2] + values[idx3]) / 4
        const avg_depth = (p0.depth + p1.depth + p2.depth + p3.depth) / 4
        
        const color = this.value_to_color(avg_value, palette, vmin, vmax)
        
        quads.push({
          depth: avg_depth,
          points: [p0, p1, p2, p3],
          color: color
        })
      }
    }
    
    // Sort back to front
    quads.sort((a, b) => a.depth - b.depth)
    
    // Draw
    for (const quad of quads) {
      ctx.fillStyle = quad.color
      ctx.strokeStyle = '#306998'
      ctx.lineWidth = 0.5
      ctx.globalAlpha = 0.9  // Use globalAlpha for transparency
      
      ctx.beginPath()
      ctx.moveTo(quad.points[0].x, quad.points[0].y)
      ctx.lineTo(quad.points[1].x, quad.points[1].y)
      ctx.lineTo(quad.points[2].x, quad.points[2].y)
      ctx.lineTo(quad.points[3].x, quad.points[3].y)
      ctx.closePath()
      ctx.fill()
      ctx.stroke()
      
      ctx.globalAlpha = 1.0  // Reset alpha
    }
  }

  private get_palette(): string[] {
    const name = this.model.palette
    
    if (name === 'Turbo256') return Turbo256
    if (name === 'Viridis256') return Viridis256
    if (name === 'Plasma256') return Plasma256
    if (name === 'Inferno256') return Inferno256
    if (name === 'Cividis256') return Cividis256
    
    return Turbo256
  }

  private get_value_range(): {vmin: number, vmax: number} {
    let vmin = this.model.vmin
    let vmax = this.model.vmax
    
    if (isNaN(vmin) || isNaN(vmax)) {
      const values = this.model.values.filter((v: number) => !isNaN(v))
      if (values.length > 0) {
        if (isNaN(vmin)) vmin = Math.min(...values)
        if (isNaN(vmax)) vmax = Math.max(...values)
      } else {
        vmin = 0
        vmax = 1
      }
    }
    
    return {vmin, vmax}
  }

  private value_to_color(value: number, palette: string[], vmin: number, vmax: number): string {
    if (isNaN(value)) {
      return this.model.nan_color
    }
    
    const normalized = (value - vmin) / (vmax - vmin)
    const idx = Math.floor(normalized * (palette.length - 1))
    const clamped_idx = Math.max(0, Math.min(palette.length - 1, idx))
    
    return palette[clamped_idx]
  }

  private draw_coastlines_sphere(cos_angle: number, sin_angle: number,
                                 cos_tilt: number, sin_tilt: number, scale: number, cx: number, cy: number): void {
    if (!this.ctx) return
    
    const ctx = this.ctx
    const coast_lons = this.model.coast_lons
    const coast_lats = this.model.coast_lats
    
    ctx.strokeStyle = this.model.coastline_color
    ctx.lineWidth = this.model.coastline_width
    
    ctx.beginPath()
    let drawing = false
    
    for (let i = 0; i < coast_lons.length; i++) {
      if (coast_lons[i] === null) {
        drawing = false
        continue
      }
      
      const lat_rad = coast_lats[i] * Math.PI / 180
      const lon_rad = coast_lons[i] * Math.PI / 180
      
      const x = Math.cos(lat_rad) * Math.cos(-lon_rad)
      const y = Math.cos(lat_rad) * Math.sin(-lon_rad)
      const z = Math.sin(lat_rad)
      
      const x_rot = x * cos_angle - y * sin_angle
      const y_rot = x * sin_angle + y * cos_angle
      const y_tilt = y_rot * cos_tilt - z * sin_tilt
      const z_tilt = y_rot * sin_tilt + z * cos_tilt
      
      if (y_tilt > -0.05) {
        const px = cx + x_rot * scale
        const py = cy - z_tilt * scale
        
        if (!drawing) {
          ctx.moveTo(px, py)
          drawing = true
        } else {
          ctx.lineTo(px, py)
        }
      } else {
        drawing = false
      }
    }
    
    ctx.stroke()
  }

  private draw_coastlines_map(proj_type: string, scale: number, cx: number, cy: number, rotation: number = 0): void {
    if (!this.ctx) return
    
    const ctx = this.ctx
    const coast_lons = this.model.coast_lons
    const coast_lats = this.model.coast_lats
    
    ctx.strokeStyle = this.model.coastline_color
    ctx.lineWidth = this.model.coastline_width
    
    ctx.beginPath()
    let drawing = false
    
    for (let i = 0; i < coast_lons.length; i++) {
      if (coast_lons[i] === null) {
        drawing = false
        continue
      }
      
      // Apply rotation
      const rotated_lon = coast_lons[i] - rotation
      
      let proj
      if (proj_type === 'mollweide') {
        proj = this.project_mollweide(rotated_lon, coast_lats[i])
      } else if (proj_type === 'natural_earth') {
        proj = this.project_natural_earth(rotated_lon, coast_lats[i])
      } else if (proj_type === 'plate_carree') {
        proj = this.project_plate_carree(rotated_lon, coast_lats[i])
      } else {
        continue
      }
      
      const px = cx + proj.x * scale
      const py = cy - proj.y * scale
      
      if (!drawing) {
        ctx.moveTo(px, py)
        drawing = true
      } else {
        ctx.lineTo(px, py)
      }
    }
    
    ctx.stroke()
  }

  private start_animation(): void {
    const animate = () => {
      if (!this.model.autorotate || this.model.projection !== 'sphere') return
      
      // Update the model's rotation directly (continues from current position)
      this.model.rotation = (this.model.rotation + this.model.rotation_speed * 0.5) % 360
      
      this.animation_id = requestAnimationFrame(animate)
    }
    
    animate()
  }

  private stop_animation(): void {
    if (this.animation_id !== undefined) {
      cancelAnimationFrame(this.animation_id)
      this.animation_id = undefined
    }
  }

  private update_tooltip(): void {
    if (!this.tooltip_el || !this.canvas) return
    
    // Get pixel data at mouse position
    const imageData = this.ctx!.getImageData(this.mouse_x, this.mouse_y, 1, 1)
    const pixel = imageData.data
    
    // Check if we're on the globe (not black background)
    if (pixel[0] > 10 || pixel[1] > 10 || pixel[2] > 10) {
      // Find approximate value based on color
      const palette = this.get_palette()
      const {vmin, vmax} = this.get_value_range()
      
      let closest_idx = 0
      let min_distance = Infinity
      
      for (let i = 0; i < palette.length; i++) {
        const pal_r = parseInt(palette[i].slice(1, 3), 16)
        const pal_g = parseInt(palette[i].slice(3, 5), 16)
        const pal_b = parseInt(palette[i].slice(5, 7), 16)
        
        const distance = Math.abs(pal_r - pixel[0]) + Math.abs(pal_g - pixel[1]) + Math.abs(pal_b - pixel[2])
        
        if (distance < min_distance) {
          min_distance = distance
          closest_idx = i
        }
      }
      
      const value = vmin + (closest_idx / (palette.length - 1)) * (vmax - vmin)
      
      this.tooltip_el.innerHTML = `Value: ${value.toFixed(2)}`
      this.tooltip_el.style.display = 'block'
      this.tooltip_el.style.left = `${this.mouse_x + 15}px`
      this.tooltip_el.style.top = `${this.mouse_y - 30}px`
    } else {
      this.tooltip_el.style.display = 'none'
    }
  }

  override remove(): void {
    this.stop_animation()
    super.remove()
  }
}

export namespace SurfaceGlobe {
  export type Attrs = p.AttrsOf<Props>

  export type Props = LayoutDOM.Props & {
    lons: p.Property<number[]>
    lats: p.Property<number[]>
    values: p.Property<number[]>
    n_lat: p.Property<number>
    n_lon: p.Property<number>
    projection: p.Property<string>
    palette: p.Property<string>
    vmin: p.Property<number>
    vmax: p.Property<number>
    nan_color: p.Property<string>
    rotation: p.Property<number>
    tilt: p.Property<number>
    azimuth: p.Property<number>
    zoom: p.Property<number>
    autorotate: p.Property<boolean>
    rotation_speed: p.Property<number>
    show_coastlines: p.Property<boolean>
    coastline_color: p.Property<string>
    coastline_width: p.Property<number>
    coast_lons: p.Property<any[]>
    coast_lats: p.Property<any[]>
    enable_hover: p.Property<boolean>
  }
}

export interface SurfaceGlobe extends SurfaceGlobe.Attrs {}

export class SurfaceGlobe extends LayoutDOM {
  declare properties: SurfaceGlobe.Props
  declare __view_type__: SurfaceGlobeView

  constructor(attrs?: Partial<SurfaceGlobe.Attrs>) {
    super(attrs)
  }

  static {
    this.prototype.default_view = SurfaceGlobeView

    this.define<SurfaceGlobe.Props>(({Any, Bool, Float, Int, List, String}) => ({
      lons: [ List(Float), [] ],
      lats: [ List(Float), [] ],
      values: [ List(Float), [] ],
      n_lat: [ Int, 30 ],
      n_lon: [ Int, 60 ],
      projection: [ String, 'sphere' ],
      palette: [ String, 'Turbo256' ],
      vmin: [ Float, NaN ],
      vmax: [ Float, NaN ],
      nan_color: [ String, '#808080' ],
      rotation: [ Float, 0 ],
      tilt: [ Float, 0 ],
      azimuth: [ Float, 0 ],
      zoom: [ Float, 1.0 ],
      autorotate: [ Bool, false ],
      rotation_speed: [ Float, 1.0 ],
      show_coastlines: [ Bool, true ],
      coastline_color: [ String, '#000000' ],
      coastline_width: [ Float, 1.2 ],
      coast_lons: [ List(Any), [] ],
      coast_lats: [ List(Any), [] ],
      enable_hover: [ Bool, true ],
    }))
  }
}
