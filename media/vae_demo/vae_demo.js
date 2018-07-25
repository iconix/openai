// based on: https://github.com/worldmodels/worldmodels.github.io/blob/a45921d53bf662830acc43169d8efd356eb5d8f7/demo/vae_demo.js

var vae_demo = function(settings) {
  "use strict"

  var vae_sketch = function( p ) {
    "use strict"

    function randi(a, b) { return Math.floor(Math.random()*(b-a)+a); }

    var div_name = settings.div_name
    var slider_size = 5
    var file_number = 0
    var min_range = settings.min_range
    var max_range = settings.max_range
    var N = slider_size

    var slider_pos
    var defaults
    var precomputed = []
    var train_sent
    var recon_sent

    // dom
    var canvas
    var slider = []
    var single_slider
    var random_file_button
    var random_z_button
    var reset_z_button
    var rect, origy, origx, screen_x, screen_y

    // settings
    var min_image_size = 320
    var textbox_size = 200
    var suggested_slider_width = 100
    var slider_width, slider_height

    // display_orientation
    var horizontal = true
    var train_x, train_y
    var recon_x, recon_y
    var file_button_x, file_button_y
    var z_button_x, z_button_y
    var reset_button_x, reset_button_y
    var train_desc_x, train_desc_y
    var recon_desc_x, recon_desc_y
    var z_desc_x, z_desc_y
    var slider_x = new Array(N)
    var slider_y = new Array(N)
    //var screen_width, screen_height

    // loading image event handling
    var loading_sent = false

    // resize and timing issues
    var redraw_frame = true

    function set_screen() {
      var i, j, k

      //screen_width = window.document.getElementById(div_name).parentElement.clientWidth
      //screen_height = window.document.getElementById(div_name).parentElement.clientHeight

      // make dom
      var bodyRect = document.body.getBoundingClientRect()
      rect = window.document.getElementById(div_name).getBoundingClientRect()

      origy = rect.top - bodyRect.top
      origx = rect.left - bodyRect.left

      horizontal = true

      if ((window.innerWidth - rect.left*2) < (min_image_size*2+suggested_slider_width+20) && p.frameCount > 0) {
        horizontal = false
      }

      if (horizontal) {
        //image_size = Math.max((screen_width - (suggested_slider_width+20) ) / 2, min_image_size)
        slider_width = suggested_slider_width
        screen_x = 760 //image_size*2+slider_width+20
        screen_y = 420 //image_size+100
        slider_height = screen_y / N //image_size / N
        textbox_size = (screen_x / 2) - suggested_slider_width

        recon_y = train_y = screen_y / 2
        train_x = 0
        recon_x = textbox_size+slider_width + 20

        z_button_y = file_button_y = textbox_size + 150
        file_button_x = 10
        z_button_x = textbox_size + 10

        reset_button_x = z_button_x + 17
        reset_button_y = z_button_y + 25

        for(i=0;i<N;i++) {
          slider_x[i] = textbox_size + 7.5
          slider_y[i] = 55 + i*slider_height
        }

        train_desc_x = textbox_size / 3
        train_desc_y = 35
        z_desc_x = (slider_width / 2) + textbox_size
        z_desc_y = 35
        recon_desc_x = textbox_size + slider_width + (textbox_size / 3)
        recon_desc_y = 35

      } else {
        // likely to be mobile or a thin vertical browser session.
        textbox_size = min_image_size
        slider_height = 25
        screen_x = 760 //Math.max(image_size, screen_width)
        screen_y = 420 //image_size*2+5*slider_height+175
        slider_width = (textbox_size)/3 - 10

        train_x = (screen_x-textbox_size) / 2
        train_y = screen_y / 2

        train_desc_x = train_x
        train_desc_y = 35

        file_button_x = train_x+(textbox_size/4)
        file_button_y = textbox_size+60

        recon_x = (screen_x-textbox_size)/2
        recon_y = screen_y - textbox_size

        recon_desc_x = recon_x
        recon_desc_y = textbox_size*1+160+0+slider_height*5

        z_button_x = recon_x+(textbox_size/3)
        z_button_y = textbox_size + 108 + slider_height*5

        reset_button_x = z_button_x + 17
        reset_button_y = z_button_y + 25

        z_desc_x = train_x+10
        z_desc_y = textbox_size+85

        k = 0
        for(i=0;i<3;i++) {
          for(j=0;j<5;j++) {
            slider_x[k] = recon_x+5+(slider_width+10)*i
            slider_y[k] = textbox_size+100+j*slider_height
            k += 1
          }
        }

      }

    }

    function draw_sliders() {
      var i
      for(i=0;i<N;i++) {
        slider[i].style('width', slider_width+'px')
        slider[i].position(origx+slider_x[i], origy+slider_y[i])
      }
    }

    function set_sliders() {
      var i
      for(i=0; i<N; i++) {
        slider[i].value(slider_pos[i])
      }
    }

    function get_sliders() {
      var i
      var new_slider = new Array(slider_size)
      for(i=0; i<N; i++) {
        new_slider[i] = slider[i].value()
      }
      return new_slider
    }

    function update_text() {
      //load_train(data, file_number)
      load_reconstruct(slider_pos)
    }

    function redraw_screen() {
      random_file_button.position(origx+file_button_x, origy+file_button_y)
      random_z_button.position(origx+z_button_x, origy+z_button_y)
      reset_z_button.position(origx+reset_button_x, origy+reset_button_y)

      draw_sliders()
      update_text()

      p.fill(0, 0, 0)
      p.textSize(16)
      p.text("Train Text", train_desc_x, train_desc_y)

      p.textSize(16)
      p.text("z", z_desc_x, z_desc_y)

      p.textSize(16)
      p.text("Reconstruction", recon_desc_x, recon_desc_y)

      loading_sent = true

    }

    function random_file_button_event() {
      redraw_frame = true
      load_random_sent()
      loading_sent = true
    }

    function random_slider() {
      var r = []
      for (var i=0;i<N;i++) {
        r.push(randi(0, 3))
      }

      return r
    }

    function random_z_button_event() {
      slider_pos = random_slider()

      set_sliders()
      draw_sliders()
      update_text()
    }

    function reset_z_button_event() {
      load_defaults()
      update_text()
    }

    function load_train() {
      train_sent = defaults[0][file_number].replace(/ EOS/g, '').trim()
    }

    function load_reconstruct() {
      if (!precomputed[file_number]) {
        $.getJSON( settings.data_dir+file_number+".json", function( data ) {
          precomputed[file_number] = data

          slider_pos.forEach(i => {
            data = data[i]
          })

          recon_sent = data.replace(/EOS /g, '').trim()
        })
      } else {
        var data = precomputed[file_number]

        slider_pos.forEach(i => {
          data = data[i]
        })

        recon_sent = data.replace(/EOS /g, '').trim()
      }
    }

    function load_defaults() {
      if (!defaults) {
        $.getJSON( settings.data_dir + "defaults.json", function( data ) {
          defaults = data

          slider_pos = defaults[1][file_number]

          set_sliders()

          load_train()
          load_reconstruct()
        })
      } else {
        slider_pos = defaults[1][file_number]

        set_sliders()

        load_train()
        load_reconstruct()
      }
    }

    function load_random_sent() {
      file_number = randi(min_range, max_range)
      load_defaults()
      loading_sent = true
    }

    function reset_screen() {
      set_screen()
      p.resizeCanvas(screen_x, screen_y)
      redraw_screen()
    }

    p.setup = function() {
      set_screen()

      load_random_sent()

      random_file_button = p.createButton('Load Random Sentence')
      random_file_button.mousePressed(random_file_button_event)
      random_z_button = p.createButton('Randomize z')
      random_z_button.mousePressed(random_z_button_event)
      reset_z_button = p.createButton('Reset z')
      reset_z_button.mousePressed(reset_z_button_event)

      canvas = p.createCanvas(screen_x, screen_y)

      for (var i=0; i<N; i++) {
        single_slider = p.createSlider(0, 2, 0, 1)
        single_slider.input(slider_event)
        slider.push(single_slider)
      }

      redraw_screen()

      p.frameRate(30)
    }

    p.draw = function() {
      if ((p.frameCount) % 30 == 0) {
        redraw_frame = true
      }
      if (redraw_frame) {
        redraw_frame = false
        reset_screen()
        redraw_screen()
      }
      if (loading_sent && train_sent && recon_sent) {
        loading_sent = false

        p.fill(0, 102, 153)
        p.textSize(20)
        p.text(train_sent, train_x, train_y, textbox_size)

        p.textSize(20)
        p.text(recon_sent, recon_x, recon_y, textbox_size)
      }
    }

    p.windowResized = function() {
      reset_screen()
    }

    function slider_event() {
      slider_pos = get_sliders()
      update_text()
    }

  }
  return vae_sketch
}
