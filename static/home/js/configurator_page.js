
// constants!
const BIGGEST_STROKE = 6;
const BIG_STROKE = 4;
const SMALL_STROKE = 2;
const CELL_WIDTH = 45;
const CELL_HEIGHT = 50;

const DOOR_MIN = 4;

const HANDLE_INDUSTRIAL_OFFSET = 7;
const HANDLE_VINTAGE_OFFSET = 0;
const HANDLE_VINTAGE_RADIUS = 8.5;
const HANDLE_GLAMOUR_OFFSET = 0.2;
const HANDLE_GLAMOUR_SIZE = 12.5;

const DOOR_FRAME_OFFSET = 0.15;
const HINGE_OFFSET = 1.0;
const HINGE_WIDTH = 4;
const HINGE_HEIGHT = 6.2;

const PIVOT_HEIGHT = 8;
const PIVOT_WIDTH = 4;
const PIVOT_OFFSET = 10;

const SIZE_MULTIPLIER = 1;


const HINGED_LIMS = {
    sides: ['left','right','both'],
    allowTop: true,
    allowLeft: true,
    allowRight: true,
    topMax: {x: 4, y: 1},
    leftMax: {x: 6, y: 5},
    doorMax: {x: 4, y: 4},
    rightMax: {x: 6, y: 5},
};
const SLIDING_LIMS = {
    sides: ['left','right','both'],
    allowTop: false,
    allowLeft: true,
    allowRight: true,
    topMax: {x: 0, y: 0},
    leftMax: {x: 6, y: 5},
    doorMax: {x: 2, y: 5},
    rightMax: {x: 6, y: 5},
};
const PIVOT_LIMS = {
    sides: ['left','right'],
    allowTop: false,
    allowLeft: true,
    allowRight: true,
    topMax: {x: 0, y: 0},
    leftMax: {x: 6, y: 5},
    doorMax: {x: 2, y: 5},
    rightMax: {x: 6, y: 5},
};
const FOLDING_LIMS = {
    sides: ['left','right'],
    allowTop: false,
    allowLeft: false,
    allowRight: false,
    topMax: {x: 0, y: 0},
    leftMax: {x: 0, y: 0},
    doorMax: {x: 10, y: 5},
    rightMax: {x: 0, y: 0},
};
const FIXED_LIMS = {
    sides: [''],
    allowTop: false,
    allowLeft: false,
    allowRight: false,
    topMax: {x: 0, y: 0},
    leftMax: {x: 0, y: 0},
    doorMax: {x: 10, y: 5},
    rightMax: {x: 0, y: 0},
};

const HINGED_DEFAULTS = {
    isSkylightEnabled: true,
    isWindowsLeftEnabled: true,
    isWindowsRightEnabled: true,
    doorSide: 'right',
    skylightCells: {x: 2, y: 1},
    doorCells: {x: 2, y: 4},
    leftCells: {x: 2, y: 5},
    rightCells: {x: 2, y: 5},



};
const SLIDING_DEFAULTS = {
    isSkylightEnabled: false,
    isWindowsLeftEnabled: true,
    isWindowsRightEnabled: true,
    doorSide: 'right',
    skylightCells: {x: 0, y: 0},
    doorCells: {x: 2, y: 5},
    leftCells: {x: 2, y: 5},
    rightCells: {x: 2, y: 5},
};
const PIVOT_DEFAULTS = {
    isSkylightEnabled: false,
    isWindowsLeftEnabled: true,
    isWindowsRightEnabled: true,
    doorSide: 'right',
    skylightCells: {x: 0, y: 0},
    doorCells: {x: 2, y: 5},
    leftCells: {x: 2, y: 5},
    rightCells: {x: 2, y: 5},
};
const FOLDING_DEFAULTS = {
    isSkylightEnabled: false,
    isWindowsLeftEnabled: false,
    isWindowsRightEnabled: false,
    doorSide: 'right',
    skylightCells: {x: 0, y: 0},
    doorCells: {x: 8, y: 5},
    leftCells: {x: 0, y: 0},
    rightCells: {x: 0, y: 0},
};
const FIXED_DEFAULTS = {
    isSkylightEnabled: false,
    isWindowsLeftEnabled: false,
    isWindowsRightEnabled: false,
    doorSide: '',
    skylightCells: {x: 0, y: 0},
    doorCells: {x: 8, y: 5},
    leftCells: {x: 0, y: 0},
    rightCells: {x: 0, y: 0},

};

//functions
function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}
//alpine.js
function globalData() {
    const defaults = {
        initialActiveSteps: [false, false, false, false, false, false, false],
        initialCompleteSteps: [false, false, false, false, false, false, false],
        styleLine: 'industrial', //industrial, vintage, glamour
        productUsecase: '',
        productType: '', //hinged, sliding, pivot, folding, fixed
        handleType: '',
        color1: '',
        color2: '',

        customColor1Enabled: false,
        customColor2Enabled: false,

        isStyleLineConfirmed: true,
        isProductUsecaseConfirmed: false,
        isProductTypeConfirmed: false,
        isHandleConfirmed: false,
        isColor1Confirmed: false,
        isColor2Confirmed: false,
        isShapeConfirmed: false,
        isSmartHomeConfirmed: false,

        multiPointLock: false,
        contactron: false,
        actuator: false,

        isSkylightEnabled: true,
        isWindowsLeftEnabled: true,
        isWindowsRightEnabled: true,

        skylightCells: {x: 4, y: 1},
        doorCells: {x: 2, y: 5},
        leftCells: {x: 2, y: 5},
        rightCells: {x: 2, y: 5},

        doorSide: 'left', //left, right, both

        inputTotalHeight: 5,
        inputDoorWidth: 2,
        inputTotalWidth: 2,
        inputRightWidth: 2,
        inputLeftWidth: 2,

    }
    return {
        finalized: false,
        loading: false,

        selectedStyleLine: defaults.styleLine,
        selectedProductUsecase: defaults.productUsecase,
        selectedProductType: defaults.productType,
        selectedHandleType: defaults.handleType,
        selectedColor1: defaults.color1,
        customColor1: defaults.color1,
        customColor1Enabled: defaults.customColor1Enabled,
        selectedColor2: defaults.color2,
        customColor2: defaults.color2,
        customColor2Enabled: defaults.customColor2Enabled,

        isStyleLineConfirmed: defaults.isStyleLineConfirmed,
        isProductUsecaseConfirmed: defaults.isProductUsecaseConfirmed,
        isProductTypeConfirmed: defaults.isProductTypeConfirmed,
        isHandleConfirmed: defaults.isHandleConfirmed,
        isColor1Confirmed: defaults.isColor1Confirmed,
        isColor2Confirmed: defaults.isColor2Confirmed,
        isShapeConfirmed: defaults.isShapeConfirmed,
        isSmartHomeConfirmed: defaults.isSmartHomeConfirmed,
        get isStyleLineSelected() {return (this.selectedStyleLine !== '' && (this.selectedColor1 !== '' || (this.customColor1 !== '' && this.customColor1Enabled)))},
        get isProductUsecaseSelected() {return this.selectedProductUsecase !== ''},
        get isProductTypeSelected() {return this.selectedProductType !== ''},
        get isAccessorySelected() {return (this.selectedHandleType !== '' && (this.selectedColor2 !== '' || (this.customColor2 !== '' && this.customColor2Enabled)))},

        smartHome: {
            multiPointLock: defaults.multiPointLock,
            contactron: defaults.contactron,
            actuator: defaults.actuator,
        },

        shapeValues: {

            isSkylightEnabled: defaults.isSkylightEnabled,
            isWindowsRightEnabled: defaults.isWindowsRightEnabled,
            isWindowsLeftEnabled: defaults.isWindowsLeftEnabled,
            skylightCells: defaults.skylightCells,
            doorCells: defaults.doorCells,
            leftCells: defaults.leftCells,
            rightCells: defaults.rightCells,
            doorSide: defaults.doorSide,
        },

        input: {
            totalHeight: defaults.inputTotalHeight,
            totalWidth: defaults.inputTotalWidth,
            doorWidth: defaults.inputDoorWidth,
            leftWidth: defaults.inputLeftWidth,
            rightWidth: defaults.inputRightWidth,
        },
        names: {
            industrial: '',
            vintage: '',
            glamour: '',
            coldProfile: '',
            hotProfile: '',
            sliding: '',
            hinged: '',
            pivot: '',
            folding: '',
            fixed: '',
            industrial_handle1: '',
            industrial_handle2: '',
            industrial_handle3: '',
            vintage_handle1: '',
            vintage_handle2: '',
            vintage_handle3: '',
            glamour_handle1: '',
            glamour_handle2: '',
            glamour_handle3: '',
            contactron: '',
            multi_point_lock: '',
            actuator: '',

        },

        init() {
            let source = document.getElementById('styleline-industrial')
            if (source) this.names.industrial = source.textContent
            source = document.getElementById('styleline-vintage')
            if (source) this.names.vintage = source.textContent
            source = document.getElementById('styleline-glamour')
            if (source) this.names.glamour = source.textContent
            source = document.getElementById('profile-cold')
            if (source) this.names.coldProfile = source.textContent
            source = document.getElementById('profile-hot')
            if (source) this.names.hotProfile = source.textContent
            source = document.getElementById('type-sliding')
            if (source) this.names.sliding = source.textContent
            source = document.getElementById('type-hinged')
            if (source) this.names.hinged = source.textContent
            source = document.getElementById('type-pivot')
            if (source) this.names.pivot = source.textContent
            source = document.getElementById('type-folding')
            if (source) this.names.folding = source.textContent
            source = document.getElementById('type-fixed')
            if (source) this.names.fixed = source.textContent
            source = document.getElementById('industrial-handle-1')
            if (source) this.names.industrial_handle1 = source.textContent
            source = document.getElementById('industrial-handle-2')
            if (source) this.names.industrial_handle2 = source.textContent
            source = document.getElementById('industrial-handle-3')
            if (source) this.names.industrial_handle3 = source.textContent
            source = document.getElementById('vintage-handle-1')
            if (source) this.names.vintage_handle1 = source.textContent
            source = document.getElementById('vintage-handle-2')
            if (source) this.names.vintage_handle2 = source.textContent
            source = document.getElementById('vintage-handle-3')
            if (source) this.names.vintage_handle3 = source.textContent
            source = document.getElementById('glamour-handle-1')
            if (source) this.names.glamour_handle1 = source.textContent
            source = document.getElementById('glamour-handle-2')
            if (source) this.names.glamour_handle2 = source.textContent
            source = document.getElementById('glamour-handle-3')
            if (source) this.names.glamour_handle3 = source.textContent
            source = document.getElementById('contactron')
            if (source) this.names.contactron = source.textContent
            source = document.getElementById('multi-point-lock')
            if (source) this.names.multi_point_lock = source.textContent
            source = document.getElementById('actuator')
            if (source) this.names.actuator = source.textContent

        },

        activeSteps: defaults.initialActiveSteps,
        completeSteps: defaults.initialCompleteSteps,
		get smartHomeDesc() {
            let text = ''
            if (this.smartHome.multiPointLock) text += this.names.multi_point_lock;
            if (this.smartHome.contactron) text+= this.names.contactron;
            if (this.smartHome.actuator) text += this.names.actuator;

            return text;
        },
        get styleLineDesc() {
            let text = '';
            if (this.selectedStyleLine === 'industrial') text = this.names.industrial;
            if (this.selectedStyleLine === 'vintage') text = this.names.vintage;
            if (this.selectedStyleLine === 'glamour') text = this.names.glamour;
            return text;
        },
        get productUsecaseDesc() {
            let text = '';
            if (this.selectedProductUsecase === 'profile-cold') text = this.names.coldProfile;
            if (this.selectedProductUsecase === 'profile-hot') text = this.names.hotProfile;
            return text;
        },
        get productTypeDesc() {
            let text = '';
            if (this.selectedProductType === 'sliding') text = this.names.sliding;
            if (this.selectedProductType === 'hinged') text = this.names.hinged;
            if (this.selectedProductType === 'pivot') text = this.names.pivot;
            if (this.selectedProductType === 'folding') text = this.names.folding;
            if (this.selectedProductType === 'fixied') text = this.names.fixed;
            return text;
        },
        get additivesDesc() {
            let text = '';
            if (this.selectedStyleLine === 'industrial') {
                if (this.selectedHandleType === 'handle-1') text = this.names.industrial_handle1;
                if (this.selectedHandleType === 'handle-2') text = this.names.industrial_handle2;
                if (this.selectedHandleType === 'handle-3') text = this.names.industrial_handle3;
            }
            if (this.selectedStyleLine === 'glamour') {
                if (this.selectedHandleType === 'handle-1') text = this.names.glamour_handle1;
                if (this.selectedHandleType === 'handle-2') text = this.names.glamour_handle2;
                if (this.selectedHandleType === 'handle-3') text = this.names.glamour_handle3;
            }
            if (this.selectedStyleLine === 'vintage') {
                if (this.selectedHandleType === 'handle-1') text = this.names.vintage_handle1;
                if (this.selectedHandleType === 'handle-2') text = this.names.vintage_handle2;
                if (this.selectedHandleType === 'handle-3') text = this.names.vintage_handle3;
            }
            return text;
        },
        get color1Desc() {
            let text = '';
            if (this.customColor1Enabled) text = this.customColor1;
            else if (this.selectedColor1 === '7016') text = 'Anthracite Grey';
            else if (this.selectedColor1 === '7021') text = 'Black Grey';
            else if (this.selectedColor1 === '7048') text = 'Pearl Mouse Grey';
            else if (this.selectedColor1 === '1012') text = 'Lemon Yellow';
            else if (this.selectedColor1 === '1013') text = 'Oyster White';
            else if (this.selectedColor1 === '6021') text = 'Pale Green';
            else if (this.selectedColor1 === '1036') text = 'Pearl Gold';
            else if (this.selectedColor1 === '5003') text = 'Sapphire Blue';
            else if (this.selectedColor1 === '6005') text = 'Moss Green';
            else text = this.selectedColor1;

            return text;
        },
        get color2Desc() {
            let text = '';
            if (this.customColor2Enabled) text = this.customColor2;
            else if (this.selectedColor2 === '7016') text = 'Anthracite Grey';
            else if (this.selectedColor2 === '7021') text = 'Black Grey';
            else if (this.selectedColor2 === '7048') text = 'Pearl Mouse Grey';
            else if (this.selectedColor2 === '1012') text = 'Lemon Yellow';
            else if (this.selectedColor2 === '1013') text = 'Oyster White';
            else if (this.selectedColor2 === '6021') text = 'Pale Green';
            else if (this.selectedColor2 === '1036') text = 'Pearl Gold';
            else if (this.selectedColor2 === '5003') text = 'Sapphire Blue';
            else if (this.selectedColor2 === '6005') text = 'Moss Green';
            else text = this.selectedColor2;

            return text;
        },

        chooseStyleLine(name) {
            if(name) this.selectedStyleLine = name;
            this.isStyleLineConfirmed = true;
        },
        chooseProductUsecase(name) {
            if(name) this.selectedProductUsecase = name;
            this.isProductUsecaseConfirmed = true;
        },
        chooseProductType(name) {
            if(name) this.selectedProductType = name;


            let values = {};
            switch(name)
            {
                case 'hinged':
                    values = HINGED_DEFAULTS;
                    break;
                case 'sliding':
                    values = SLIDING_DEFAULTS;
                    break;
                case 'pivot':
                    values = PIVOT_DEFAULTS;
                    break;
                case 'folding':
                    values = FOLDING_DEFAULTS
                    break;
                default:
                    values = FIXED_DEFAULTS;
                    break;
            }

            this.shapeValues.isSkylightEnabled = values.isSkylightEnabled;
            this.shapeValues.isWindowsRightEnabled = values.isWindowsRightEnabled;
            this.shapeValues.isWindowsLeftEnabled = values.isWindowsLeftEnabled;
            this.shapeValues.doorSide = values.doorSide;
            this.shapeValues.doorCells.x = values.doorCells.x;
            this.shapeValues.doorCells.y = values.doorCells.y;
            this.shapeValues.leftCells.x = values.leftCells.x;
            this.shapeValues.leftCells.y = values.leftCells.y;
            this.shapeValues.rightCells.x = values.rightCells.x;
            this.shapeValues.rightCells.y = values.rightCells.y;
            this.shapeValues.skylightCells.x = values.skylightCells.x;
            this.shapeValues.skylightCells.y = values.skylightCells.y;

            this.updateInput();
            this.isProductTypeConfirmed = true;

        },
        chooseHandleType(name) {
            if(name) this.selectedHandleType = name;
            this.isHandleConfirmed = true;
        },
        chooseColor1(name) {
            if(name) this.selectedColor1 = name;
            this.isColor1Confirmed = true;
        },
        chooseColor2(name) {
            if(name) this.selectedColor2 = name;
            this.isColor2Confirmed = true;
        },
        confirmShape() {
            this.isShapeConfirmed = true;
        },
        confirmSmartHome() {
            this.isSmartHomeConfirmed = true;
        },

        confirmCustomColor1() {
            if(this.customColor1Enabled)
            {
                this.selectedColor1 = this.customColor1;
            }
        },
        confirmCustomColor2() {
            if(this.customColor2Enabled)
            {
                this.selectedColor2 = this.customColor2;
            }

        },


        switchStep(step) {
            this.activeSteps[step] = !this.activeSteps[step];
        },

        confirmStep(step) {

            switch(step) {
                case 0:
                    // if (this.selectedStyleLine !== '' && this.selectedColor1 !== '') {
					this.activeSteps[0] = false;

					if (this.completeSteps[0] === false)
					{
						this.completeSteps[0] = true;
                    	this.activeSteps[1] = true
                    }
					break;
                case 1:
                    this.activeSteps[1] = false;
					if (this.completeSteps[1] === false)
					{
						this.completeSteps[1] = true;
                    	this.activeSteps[2] = true;
					}
                    break;
                case 2:
                    this.activeSteps[2] = false;
					if (this.completeSteps[2] === false)
					{
						this.completeSteps[2] = true;
                        this.activeSteps[3] = true;
                    }
					break;
                case 3:
                    this.activeSteps[3] = false;
					if (this.completeSteps[3] === false)
					{
						this.completeSteps[3] = true;
                        this.activeSteps[4] = true;
                    }
					break;
                case 4:
                    this.activeSteps[4] = false;
					if (this.completeSteps[4] === false)
					{
						this.completeSteps[4] = true;
                        this.activeSteps[5] = true;
                    }
					break;
                case 5:
                    this.activeSteps[5] = false;
					if (this.completeSteps[5] === false)
					{
						this.completeSteps[5] = true;
	                	this.activeSteps[6] = true;
                    }
					window.scrollTo(0, 0)
                    break;
            }

            if (
                this.isStyleLineConfirmed &&
                this.isProductUsecaseConfirmed &&
                this.isProductTypeConfirmed &&
                this.isHandleConfirmed &&
                this.isColor2Confirmed &&
                this.isShapeConfirmed &&
                this.isSmartHomeConfirmed
            )
            this.finalized = true;


        },

        //shape
        updateShape() {

            if (Number(this.input.totalHeight) === DOOR_MIN)
            {
                this.shapeValues.isSkylightEnabled = false;
                this.shapeValues.doorCells.y = Number(this.input.totalHeight);
            }
            else if (Number(this.input.totalHeight) <= this.shapeLimitations.doorMax.y)
            {
                this.shapeValues.doorCells.y = Number(this.input.totalHeight);
            }
            else if (Number(this.input.totalHeight) > this.shapeLimitations.doorMax.y)
            {
                this.shapeValues.isSkylightEnabled = true;
                this.shapeValues.doorCells.y = this.shapeLimitations.doorMax.y
            }
            this.shapeValues.leftCells.y = Number(this.input.totalHeight);
            this.shapeValues.rightCells.y = Number(this.input.totalHeight);

            if (!this.shapeLimitations.allowLeft && !this.shapeLimitations.allowRight)
            {
                this.shapeValues.doorCells.x = Number(this.input.totalWidth);
            }
            else
            {
                this.shapeValues.doorCells.x = Number(this.input.doorWidth);
            }

            if(this.shapeValues.isWindowsLeftEnabled)
            {
                this.shapeValues.leftCells.x = Number(this.input.leftWidth);

            }
            if(this.shapeValues.isWindowsRightEnabled)
            {
                this.shapeValues.rightCells.x = Number(this.input.rightWidth);

            }




        },

        get shapeLimitations() {
            //hinged, sliding, pivot, folding, fixed
            let limitations = {};
            switch(this.selectedProductType) {
                case 'hinged':
                    limitations = {...HINGED_LIMS}
                    break;
                case 'sliding':
                    limitations = {...SLIDING_LIMS}
                    break;
                case 'pivot':
                    limitations = {...PIVOT_LIMS}
                    break;
                case 'folding':
                    limitations = {...FOLDING_LIMS}
                    break;
                default: //fixed
                    limitations = {...FIXED_LIMS}
                    break;
            }
            return limitations;
        },

        get industrialHandleOffset() {
            return HANDLE_INDUSTRIAL_OFFSET * SIZE_MULTIPLIER;
        },
        get vintageHandleOffset() {
            return HANDLE_VINTAGE_OFFSET * SIZE_MULTIPLIER;
        },
        get vintageRadius() {
            return HANDLE_VINTAGE_RADIUS * SIZE_MULTIPLIER;
        },
        get glamourHandleSize() {
            return HANDLE_GLAMOUR_SIZE * SIZE_MULTIPLIER;
        },

        get glamourHandleOffset() {
            return HANDLE_GLAMOUR_OFFSET * SIZE_MULTIPLIER;
        },

        get hingeHeight() {
            return HINGE_HEIGHT * SIZE_MULTIPLIER;
        },
        get hingeWidth() {
            return HINGE_WIDTH * SIZE_MULTIPLIER;
        },
        get hingeOffset() {
            return HINGE_OFFSET * SIZE_MULTIPLIER;
        },
        get pivotOffset() {
            return PIVOT_OFFSET * SIZE_MULTIPLIER;
        },
        get pivotHeight() {
            return PIVOT_HEIGHT * SIZE_MULTIPLIER;
        },
        get pivotWidth() {
            return PIVOT_WIDTH * SIZE_MULTIPLIER;
        },

        get cellWidth() {
            return CELL_WIDTH * SIZE_MULTIPLIER;
        },
        get cellHeight() {
            return CELL_HEIGHT * SIZE_MULTIPLIER;
        },

        get grid() {
            const horizontal = this.shapeValues.doorCells.y +
                (this.shapeValues.isSkylightEnabled ? this.shapeValues.skylightCells.y : 0);
            const vertical = this.shapeValues.doorCells.x +
                (this.shapeValues.doorSide === 'both' ? this.shapeValues.doorCells.x : 0) +
                (this.shapeValues.isWindowsLeftEnabled ? this.shapeValues.leftCells.x : 0) +
                (this.shapeValues.isWindowsRightEnabled ? this.shapeValues.rightCells.x : 0);

            return {x: vertical, y: horizontal};
        },
        get leftDoorPosition() {
            let pos = 0;
            if (this.shapeValues.isWindowsLeftEnabled) {
                pos += this.shapeValues.leftCells.x;
            }
            return pos;
        },
        get rightDoorPosition() {
            let pos = this.shapeValues.doorCells.x;
            if (this.shapeValues.isWindowsLeftEnabled) {
                pos += this.shapeValues.leftCells.x;
            }
            if (this.shapeValues.doorSide === 'both') {
                pos += this.shapeValues.doorCells.x;
            }
            return pos;
        },
        get doorMiddlePosition() {
            let pos = 0;
            if (this.shapeValues.isWindowsLeftEnabled) {
                pos += this.shapeValues.leftCells.x;
            }
            if (this.shapeValues.doorSide === 'both') {
                pos += this.shapeValues.doorCells.x;
            }
            return pos;
        },
        get topDoorPosition() {
            let pos = 0;
            if (this.shapeValues.isSkylightEnabled) {
                pos += this.shapeValues.skylightCells.y;
            }
            return pos;
        },

        get productHeight() {
            return this.grid.y * this.cellHeight;
        },
        get productWidth() {
            return this.grid.x * this.cellWidth;
        },

        get leftWidth() {
            return this.shapeValues.leftCells.x * this.cellWidth;
        },

        get rightWidth() {
            return this.shapeValues.rightCells.x * this.cellWidth;
        },

        get doorWidth() {
            if(this.shapeValues.isWindowsLeftEnabled && this.shapeValues.isWindowsRightEnabled)
                return this.productWidth - this.rightWidth - this.leftWidth;
            else if(this.shapeValues.isWindowsLeftEnabled)
                return this.productWidth - this.leftWidth;
            else if(this.shapeValues.isWindowsRightEnabled)
                return this.productWidth - this.rightWidth;
            else
                return this.productWidth;

        },


        get svgOffset() {
            return BIG_STROKE * SIZE_MULTIPLIER;
        },
        get svgStrokeDownset() {
            return DOOR_FRAME_OFFSET * BIG_STROKE * SIZE_MULTIPLIER;
        },
        get svgBiggestStroke() {
            return BIGGEST_STROKE * SIZE_MULTIPLIER;
        },
        get svgBigStroke() {
            return BIG_STROKE * SIZE_MULTIPLIER;
        },
        get svgSmallStroke() {
            return SMALL_STROKE * SIZE_MULTIPLIER;
        },
        get svgHeight() {
            return (this.productHeight + (2 * this.svgBigStroke));
        },
        get svgWidth() {
            return (this.productWidth + (2 * this.svgBigStroke));
        },


        get svgGrid() {
            const lines = [];
            //pionowe
            for (let i = 1; i < this.grid.x; i++)
            {

                if (i === this.leftDoorPosition || i === this.rightDoorPosition)
                {
                    lines.push(`
                            <line
                                x1="${this.svgOffset + (i * this.cellWidth)}"
                                x2="${this.svgOffset + (i * this.cellWidth)}"
                                y1="0"
                                y2="${this.svgHeight}"
                                stroke="black" stroke-width="${this.svgBigStroke}"
                            />
                        `);
                }
                else if(i === this.doorMiddlePosition && this.shapeValues.doorSide === 'both')
                {
                    lines.push(`
                            <line
                                x1="${this.svgOffset + (i * this.cellWidth)}"
                                x2="${this.svgOffset + (i * this.cellWidth)}"
                                y1="0"
                                y2="${this.svgOffset + (this.topDoorPosition * this.cellHeight)}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `);
                    lines.push(`
                            <line
                                x1="${this.svgOffset + (i * this.cellWidth)}"
                                x2="${this.svgOffset + (i * this.cellWidth)}"
                                y1="${this.svgOffset + (this.topDoorPosition * this.cellHeight)}"
                                y2="${this.svgHeight}"
                                stroke="black" stroke-width="${this.svgBiggestStroke}"
                            />
                        `);
                }
                else if (this.selectedProductType === 'folding' && i%2 === 0)
                {
                    lines.push(`
                            <line
                                x1="${this.svgOffset + (i * this.cellWidth)}"
                                x2="${this.svgOffset + (i * this.cellWidth)}"
                                y1="0"
                                y2="${this.svgHeight}"
                                stroke="black" stroke-width="${this.svgBigStroke}"
                            />
                        `);
                }
                else if (this.selectedStyleLine === 'vintage' && i%2 === 1)
                {
                    lines.push(`
                            <line
                                x1="${this.svgOffset + (i * this.cellWidth)}"
                                x2="${this.svgOffset + (i * this.cellWidth)}"
                                y1="0"
                                y2="${this.svgOffset + ((this.grid.y-1) * this.cellHeight)}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `);

                }
                else
                {
                    lines.push(`
                            <line
                                x1="${this.svgOffset + (i * this.cellWidth)}"
                                x2="${this.svgOffset + (i * this.cellWidth)}"
                                y1="0"
                                y2="${this.svgHeight}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `);
                }

            }
            //poziome
            for (let i = 0; i <= this.grid.y; i++)
            {
                if (i === 0 && this.selectedProductType !== 'sliding' && this.selectedProductType !== 'pivot' && this.selectedProductType !== 'folding') {}
                else if (i === 0 && (this.selectedProductType === 'sliding' || this.selectedProductType === 'pivot' || this.selectedProductType === 'folding'))
                {
                    lines.push(`
                            <line
                                y1="${this.svgOffset + (i * this.cellHeight) + this.svgStrokeDownset}"
                                y2="${this.svgOffset + (i * this.cellHeight) + this.svgStrokeDownset}"
                                x1="${this.svgOffset + (this.leftDoorPosition * this.cellWidth)}"
                                x2="${this.svgOffset + (this.rightDoorPosition * this.cellWidth)}"
                                stroke="black" stroke-width="${this.svgBigStroke}"
                            />
                        `);
                }
                else if (i === this.topDoorPosition)
                {
                    if (this.shapeValues.isWindowsLeftEnabled)
                    {
                        lines.push(`
                                <line
                                    y1="${this.svgOffset + (i * this.cellHeight)}"
                                    y2="${this.svgOffset + (i * this.cellHeight)}"
                                    x1="0"
                                    x2="${this.svgOffset + (this.leftDoorPosition * this.cellWidth)}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);
                    }
                    if (this.shapeValues.isWindowsRightEnabled)
                    {
                        lines.push(`
                                <line
                                    y1="${this.svgOffset + (i * this.cellHeight)}"
                                    y2="${this.svgOffset + (i * this.cellHeight)}"
                                    x1="${this.svgOffset + (this.rightDoorPosition * this.cellWidth)}"
                                    x2="${this.svgWidth}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);
                    }
                    lines.push(`
                            <line
                                y1="${this.svgOffset + (i * this.cellHeight) + this.svgStrokeDownset}"
                                y2="${this.svgOffset + (i * this.cellHeight) + this.svgStrokeDownset}"
                                x1="${this.svgOffset + (this.leftDoorPosition * this.cellWidth)}"
                                x2="${this.svgOffset + (this.rightDoorPosition * this.cellWidth)}"
                                stroke="black" stroke-width="${this.svgBigStroke}"
                            />
                        `);
                }
                else if (i === this.grid.y && this.selectedProductType !== 'fixed')
                {
                    lines.push(`
                            <line
                                y1="${this.svgOffset + (i * this.cellHeight) - this.svgStrokeDownset}"
                                y2="${this.svgOffset + (i * this.cellHeight) - this.svgStrokeDownset}"
                                x1="${this.svgOffset + (this.leftDoorPosition * this.cellWidth)}"
                                x2="${this.svgOffset + (this.rightDoorPosition * this.cellWidth)}"
                                stroke="black" stroke-width="${this.svgBigStroke}"
                            />
                        `);

                }
                else if (this.selectedStyleLine === 'industrial')
                {
                    lines.push(`
                            <line
                                y1="${this.svgOffset + (i * this.cellHeight)}"
                                y2="${this.svgOffset + (i * this.cellHeight)}"
                                x1="0"
                                x2="${this.svgWidth}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `);
                }
                else if (this.selectedStyleLine === 'vintage' && (i === this.grid.y-1 || (i === 1 && !this.shapeValues.isSkylightEnabled)))
                {
                    lines.push(`
                            <line
                                y1="${this.svgOffset + (i * this.cellHeight)}"
                                y2="${this.svgOffset + (i * this.cellHeight)}"
                                x1="0"
                                x2="${this.svgWidth}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `);
                }
                else if (this.selectedStyleLine === 'glamour' && (i === this.grid.y-2 || (i === 1 && !this.shapeValues.isSkylightEnabled && this.shapeValues.doorCells.y > 4)))
                {
                    lines.push(`
                            <line
                                y1="${this.svgOffset + (i * this.cellHeight)}"
                                y2="${this.svgOffset + (i * this.cellHeight)}"
                                x1="0"
                                x2="${this.svgWidth}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `);
                }
            }
            //polkola i ozdobniki
            for (let i = 0; i < this.grid.x; i++)
            {
                if (this.shapeValues.isWindowsLeftEnabled && this.shapeValues.leftCells.x%2 === 1 && this.selectedStyleLine === 'vintage')
                {
                    if (i%2 === 1)
                    {
                        lines.push(`
                                <path
                                    d="
                                        M ${(i * this.cellWidth) + this.svgOffset} ${this.cellHeight + this.svgOffset}
                                        A ${this.cellWidth} ${this.cellHeight}
                                        0 0 1 ${((i+1) * this.cellWidth) + this.svgBigStroke} ${this.svgOffset}
                                    "
                                    stroke="black" stroke-width="${this.svgSmallStroke}" fill="none"
                                />
                            `);
                    }
                    else
                    {
                        lines.push(`
                            <path
                                d="
                                    M ${((i+1) * this.cellWidth) + this.svgOffset} ${this.cellHeight + this.svgOffset}
                                    A ${this.cellWidth} ${this.cellHeight}
                                    0 0 0 ${(i * this.cellWidth) + this.svgBigStroke} ${this.svgOffset}
                                "
                                stroke="black" stroke-width="${this.svgSmallStroke}" fill="none"
                            />
                            `);
                    }
                }
                else if (this.selectedStyleLine === 'vintage')
                {
                    if (i%2 === 0)
                    {
                        lines.push(`
                                <path
                                    d="
                                        M ${(i * this.cellWidth) + this.svgOffset} ${this.cellHeight + this.svgOffset}
                                        A ${this.cellWidth} ${this.cellHeight}
                                        0 0 1 ${((i+1) * this.cellWidth) + this.svgBigStroke} ${this.svgOffset}
                                    "
                                    stroke="black" stroke-width="${this.svgSmallStroke}" fill="none"
                                />
                            `);
                    }
                    else
                    {
                        lines.push(`
                            <path
                                d="
                                    M ${((i+1) * this.cellWidth) + this.svgOffset} ${this.cellHeight + this.svgOffset}
                                    A ${this.cellWidth} ${this.cellHeight}
                                    0 0 0 ${(i * this.cellWidth) + this.svgBigStroke} ${this.svgOffset}
                                "
                                stroke="black" stroke-width="${this.svgSmallStroke}" fill="none"
                            />
                            `);
                    }
                }
                else if (this.shapeValues.isWindowsLeftEnabled && this.shapeValues.leftCells.x%2 === 1 && this.selectedStyleLine === 'glamour')
                {
                    lines.push(`
                            <line
                                x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                x2="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                y1="${this.svgOffset + (0.5 * this.cellHeight)}"
                                y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `);
                    if (i%2 === 0)
                    {
                        lines.push(`
                                <line
                                    x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                    x2="${this.svgOffset + (i * this.cellWidth)}"
                                    y1="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                    y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);
                        lines.push(`
                                <line
                                    x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                    x2="${this.svgOffset + (i * this.cellWidth)}"
                                    y1="${this.svgOffset + (0.5 * this.cellHeight)}"
                                    y2="${this.svgOffset + (0.5 * this.cellHeight)}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);
                    }
                    else
                    {
                        lines.push(`
                                <line
                                    x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                    x2="${this.svgOffset + ((i+1) * this.cellWidth)}"
                                    y1="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                    y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);
                        lines.push(`
                                <line
                                    x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                    x2="${this.svgOffset + ((i+1) * this.cellWidth)}"
                                    y1="${this.svgOffset + (0.5 * this.cellHeight)}"
                                    y2="${this.svgOffset + (0.5 * this.cellHeight)}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);

                    }
                }
                else if (this.selectedStyleLine === 'glamour')
                {
                    lines.push(`
                            <line
                                x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                x2="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                y1="${this.svgOffset + (0.5 * this.cellHeight)}"
                                y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `);
                    if (i%2 === 0)
                    {
                        lines.push(`
                                <line
                                    x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                    x2="${this.svgOffset + ((i+1) * this.cellWidth)}"
                                    y1="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                    y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);
                        lines.push(`
                                <line
                                    x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                    x2="${this.svgOffset + ((i+1) * this.cellWidth)}"
                                    y1="${this.svgOffset + (0.5 * this.cellHeight)}"
                                    y2="${this.svgOffset + (0.5 * this.cellHeight)}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);
                    }
                    else
                    {
                        lines.push(`
                                <line
                                    x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                    x2="${this.svgOffset + (i * this.cellWidth)}"
                                    y1="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                    y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight)}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);
                        lines.push(`
                                <line
                                    x1="${this.svgOffset + ((i+0.5) * this.cellWidth)}"
                                    x2="${this.svgOffset + (i * this.cellWidth)}"
                                    y1="${this.svgOffset + (0.5 * this.cellHeight)}"
                                    y2="${this.svgOffset + (0.5 * this.cellHeight)}"
                                    stroke="black" stroke-width="${this.svgSmallStroke}"
                                />
                            `);

                    }
                }
            }


            return lines.join('\n');
        },

        get svgDoorHandles() {
            let handle = ``;
            if (this.shapeValues.doorSide === 'right' && this.selectedProductType !== 'fixed')
            {
                if (this.selectedStyleLine === 'industrial')
                {
                    handle =`
                            <line
                                x1="${this.svgOffset + this.industrialHandleOffset + (this.leftDoorPosition * this.cellWidth)}"
                                x2="${this.svgOffset + this.industrialHandleOffset + (this.leftDoorPosition * this.cellWidth)}"
                                y1="${this.svgOffset + ((this.grid.y-3) * this.cellHeight)}"
                                y2="${this.svgHeight}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `;
                }
                else if(this.selectedStyleLine === 'vintage')
                {
                    handle =`
                            <path
                                d="
                                    M
                                    ${this.svgOffset + (this.leftDoorPosition * this.cellWidth) + this.vintageHandleOffset}
                                    ${this.svgOffset + ((this.grid.y-2) * this.cellHeight + this.vintageRadius)}
                                    A ${this.vintageRadius} ${this.vintageRadius}
                                    0 0 0
                                    ${this.svgOffset + (this.leftDoorPosition * this.cellWidth) + this.vintageHandleOffset}
                                    ${this.svgOffset + ((this.grid.y-2) * this.cellHeight - this.vintageRadius)}
                                "
                                fill="black"
                            />
                        `
                }
                else if (this.selectedStyleLine === 'glamour')
                {
                    handle = `
                            <rect
                                x="${this.svgOffset + (this.leftDoorPosition * this.cellWidth) - this.glamourHandleOffset}"
                                y="${this.svgOffset + ((this.grid.y-2) * this.cellHeight) - (this.glamourHandleSize/2)}"
                                width="${this.glamourHandleSize}"
                                height="${this.glamourHandleSize}"
                                fill="black"
                            />
                        `
                }
            }
            else if (this.shapeValues.doorSide === 'left' && this.selectedProductType !== 'fixed')
            {
                if (this.selectedStyleLine === 'industrial')
                {
                    handle =`
                            <line
                                x1="${this.svgOffset - this.industrialHandleOffset + (this.rightDoorPosition * this.cellWidth)}"
                                x2="${this.svgOffset - this.industrialHandleOffset + (this.rightDoorPosition * this.cellWidth)}"
                                y1="${this.svgOffset + ((this.grid.y-3) * this.cellHeight)}"
                                y2="${this.svgHeight}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `;
                }
                else if(this.selectedStyleLine === 'vintage')
                {
                    handle =`
                            <path
                                d="
                                    M
                                    ${this.svgOffset + (this.rightDoorPosition * this.cellWidth) - this.vintageHandleOffset}
                                    ${this.svgOffset + ((this.grid.y-2) * this.cellHeight + this.vintageRadius)}
                                    A ${this.vintageRadius} ${this.vintageRadius}
                                    0 0 1
                                    ${this.svgOffset + (this.rightDoorPosition * this.cellWidth) - this.vintageHandleOffset}
                                    ${this.svgOffset + ((this.grid.y-2) * this.cellHeight - this.vintageRadius)}
                                "
                                fill="black"
                            />
                        `
                }
                else if (this.selectedStyleLine === 'glamour')
                {
                    handle = `
                            <rect
                                x="${this.svgOffset + (this.rightDoorPosition * this.cellWidth) - this.glamourHandleSize + this.glamourHandleOffset}"
                                y="${this.svgOffset + ((this.grid.y-2) * this.cellHeight) - (this.glamourHandleSize/2)}"
                                width="${this.glamourHandleSize}"
                                height="${this.glamourHandleSize}"
                                fill="black"
                            />
                        `
                }
            }
            else if (this.selectedProductType !== 'fixed')
            {
                if (this.selectedStyleLine === 'industrial')
                {
                    handle =`
                            <line
                                x1="${this.svgOffset - this.industrialHandleOffset + (this.doorMiddlePosition * this.cellWidth)}"
                                x2="${this.svgOffset - this.industrialHandleOffset + (this.doorMiddlePosition * this.cellWidth)}"
                                y1="${this.svgOffset + ((this.grid.y-3) * this.cellHeight)}"
                                y2="${this.svgHeight}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                            <line
                                x1="${this.svgOffset + this.industrialHandleOffset + (this.doorMiddlePosition * this.cellWidth)}"
                                x2="${this.svgOffset + this.industrialHandleOffset + (this.doorMiddlePosition * this.cellWidth)}"
                                y1="${this.svgOffset + ((this.grid.y-3) * this.cellHeight)}"
                                y2="${this.svgHeight}"
                                stroke="black" stroke-width="${this.svgSmallStroke}"
                            />
                        `;
                }
                else if (this.selectedStyleLine === 'vintage')
                {
                    handle =`
                            <path
                                d="
                                    M
                                    ${this.svgOffset + (this.doorMiddlePosition * this.cellWidth) - this.vintageHandleOffset}
                                    ${this.svgOffset + ((this.grid.y-2) * this.cellHeight + this.vintageRadius)}
                                    A ${this.vintageRadius} ${this.vintageRadius}
                                    0 0 1
                                    ${this.svgOffset + (this.doorMiddlePosition * this.cellWidth) - this.vintageHandleOffset}
                                    ${this.svgOffset + ((this.grid.y-2) * this.cellHeight - this.vintageRadius)}
                                "
                                fill="black"
                            />
                            <path
                                d="
                                    M
                                    ${this.svgOffset + (this.doorMiddlePosition * this.cellWidth) + this.vintageHandleOffset}
                                    ${this.svgOffset + ((this.grid.y-2) * this.cellHeight + this.vintageRadius)}
                                    A ${this.vintageRadius} ${this.vintageRadius}
                                    0 0 0
                                    ${this.svgOffset + (this.doorMiddlePosition * this.cellWidth) + this.vintageHandleOffset}
                                    ${this.svgOffset + ((this.grid.y-2) * this.cellHeight - this.vintageRadius)}
                                "
                                fill="black"
                            />
                        `
                }
                else if(this.selectedStyleLine === 'glamour')
                {
                    handle = `
                            <rect
                                x="${this.svgOffset + (this.doorMiddlePosition * this.cellWidth) - this.glamourHandleOffset}"
                                y="${this.svgOffset + ((this.grid.y-2) * this.cellHeight) - (this.glamourHandleSize/2)}"
                                width="${this.glamourHandleSize}"
                                height="${this.glamourHandleSize}"
                                fill="black"
                            />
                            <rect
                                x="${this.svgOffset + (this.doorMiddlePosition * this.cellWidth) - this.glamourHandleSize + this.glamourHandleOffset}"
                                y="${this.svgOffset + ((this.grid.y-2) * this.cellHeight) - (this.glamourHandleSize/2)}"
                                width="${this.glamourHandleSize}"
                                height="${this.glamourHandleSize}"
                                fill="black"
                            />
                        `
                }
            }
            return handle;
        },

        get svgDoorHinges() {
            let hinges = ``
            if (this.shapeValues.doorSide === 'right' && this.selectedProductType === 'hinged')
            {
                hinges = `
                        <line
                            x1="${this.svgOffset - this.hingeOffset + (this.rightDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset - this.hingeOffset + (this.rightDoorPosition * this.cellWidth)}"
                            y1="${this.svgOffset + ((this.topDoorPosition+0.5) * this.cellHeight) - this.hingeHeight}"
                            y2="${this.svgOffset + ((this.topDoorPosition+0.5) * this.cellHeight) + this.hingeHeight}"
                            stroke="black" stroke-width="${this.hingeWidth}"
                        />
                        <line
                            x1="${this.svgOffset - this.hingeOffset + (this.rightDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset - this.hingeOffset + (this.rightDoorPosition * this.cellWidth)}"
                            y1="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight) - this.hingeHeight}"
                            y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight) + this.hingeHeight}"
                            stroke="black" stroke-width="${this.hingeWidth}"
                        />
                    `
            }
            else if (this.shapeValues.doorSide === 'left' && this.selectedProductType === 'hinged')
            {
                hinges = `
                        <line
                            x1="${this.svgOffset + this.hingeOffset + (this.leftDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset + this.hingeOffset + (this.leftDoorPosition * this.cellWidth)}"
                            y1="${this.svgOffset + ((this.topDoorPosition+0.5) * this.cellHeight) - this.hingeHeight}"
                            y2="${this.svgOffset + ((this.topDoorPosition+0.5) * this.cellHeight) + this.hingeHeight}"
                            stroke="black" stroke-width="${this.hingeWidth}"
                        />
                        <line
                            x1="${this.svgOffset + this.hingeOffset + (this.leftDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset + this.hingeOffset + (this.leftDoorPosition * this.cellWidth)}"
                            y1="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight) - this.hingeHeight}"
                            y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight) + this.hingeHeight}"
                            stroke="black" stroke-width="${this.hingeWidth}"
                        />
                    `
            }
            else if (this.selectedProductType === 'hinged')
            {
                hinges = `
                        <line
                            x1="${this.svgOffset - this.hingeOffset + (this.rightDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset - this.hingeOffset + (this.rightDoorPosition * this.cellWidth)}"
                            y1="${this.svgOffset + ((this.topDoorPosition+0.5) * this.cellHeight) - this.hingeHeight}"
                            y2="${this.svgOffset + ((this.topDoorPosition+0.5) * this.cellHeight) + this.hingeHeight}"
                            stroke="black" stroke-width="${this.hingeWidth}"
                        />
                        <line
                            x1="${this.svgOffset - this.hingeOffset + (this.rightDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset - this.hingeOffset + (this.rightDoorPosition * this.cellWidth)}"
                            y1="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight) - this.hingeHeight}"
                            y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight) + this.hingeHeight}"
                            stroke="black" stroke-width="${this.hingeWidth}"
                        />
                        <line
                            x1="${this.svgOffset + this.hingeOffset + (this.leftDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset + this.hingeOffset + (this.leftDoorPosition * this.cellWidth)}"
                            y1="${this.svgOffset + ((this.topDoorPosition+0.5) * this.cellHeight) - this.hingeHeight}"
                            y2="${this.svgOffset + ((this.topDoorPosition+0.5) * this.cellHeight) + this.hingeHeight}"
                            stroke="black" stroke-width="${this.hingeWidth}"
                        />
                        <line
                            x1="${this.svgOffset + this.hingeOffset + (this.leftDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset + this.hingeOffset + (this.leftDoorPosition * this.cellWidth)}"
                            y1="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight) - this.hingeHeight}"
                            y2="${this.svgHeight - this.svgOffset - (0.5 * this.cellHeight) + this.hingeHeight}"
                            stroke="black" stroke-width="${this.hingeWidth}"
                        />
                    `
            }
            else if (this.shapeValues.doorSide === 'right' && this.selectedProductType === 'pivot')
            {
                hinges = `
                        <line
                            x1="${this.svgOffset - this.pivotOffset + (this.rightDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset - this.pivotOffset + (this.rightDoorPosition * this.cellWidth)}"
                            y1="0"
                            y2="${this.svgOffset + this.pivotHeight}"
                            stroke="black" stroke-width="${this.pivotWidth}"
                        />
                        <line
                            x1="${this.svgOffset - this.pivotOffset + (this.rightDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset - this.pivotOffset + (this.rightDoorPosition * this.cellWidth)}"
                            y1="${this.svgHeight}"
                            y2="${this.svgHeight - this.svgOffset - this.pivotHeight}"
                            stroke="black" stroke-width="${this.pivotWidth}"
                        />
                    `
            }
            else if (this.shapeValues.doorSide === 'left' && this.selectedProductType === 'pivot')
            {
                hinges = `
                        <line
                            x1="${this.svgOffset + this.pivotOffset + (this.leftDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset + this.pivotOffset + (this.leftDoorPosition * this.cellWidth)}"
                            y1="0"
                            y2="${this.svgOffset + this.pivotHeight}"
                            stroke="black" stroke-width="${this.pivotWidth}"
                        />
                        <line
                            x1="${this.svgOffset + this.pivotOffset + (this.leftDoorPosition * this.cellWidth)}"
                            x2="${this.svgOffset + this.pivotOffset + (this.leftDoorPosition * this.cellWidth)}"
                            y1="${this.svgHeight}"
                            y2="${this.svgHeight - this.svgOffset - this.pivotHeight}"
                            stroke="black" stroke-width="${this.pivotWidth}"
                        />
                    `
            }

            return hinges;
        },

        get svgFillers() {
            const fillers = [''];
            if (this.selectedStyleLine === 'vintage')
            {
                fillers.push(`
                        <rect
                            x="0" y="${(this.svgOffset) + ((this.grid.y-1) * this.cellHeight)}"
                            width="${this.svgWidth}"
                            height="${this.cellHeight + this.svgOffset}"
                            stroke="none" fill="#56585B"
                        />
                    `);
            }
            return fillers.join('\n');
        },

        get svgDisplayFile() {
            //update
            this.updateLimitations();
            this.updateInput();

            return `
                    <svg
                        class="svg-display-file"
                        style="--svg-width: ${this.svgWidth}px"
                        viewBox="0 0 ${this.svgWidth} ${this.svgHeight}"
                        preserveAspectRatio="xMidYMid meet"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <rect
                            x="0" y="0"
                            width="${this.svgWidth}"
                            height="${this.svgHeight}"
                            stroke="none" fill="white"
                        />
                        ${this.svgFillers}
                        <rect
                            x="0" y="0"
                            width="${this.svgWidth}"
                            height="${this.svgHeight}"
                            stroke-width="${2 * this.svgBigStroke}"
                            stroke="black" fill="none"
                        />
                        <g>
                            ${this.svgGrid}
                            ${this.svgDoorHandles}
                            ${this.svgDoorHinges}
                        </g>
                    </svg>
                `
        },

        updateLimitations() {
            if (this.shapeValues.isSkylightEnabled && !this.shapeLimitations.allowTop) {
                this.shapeValues.isSkylightEnabled = false;
                this.shapeValues.doorCells.y = Number(this.input.totalHeight);
            }
            if (this.shapeValues.isWindowsLeftEnabled && !this.shapeLimitations.allowLeft) this.shapeValues.isWindowsLeft = false;
            if (this.shapeValues.isWindowsRightEnabled && !this.shapeLimitations.allowRight) this.shapeValues.isWindowsRight = false;
            if (this.shapeValues.leftCells.y > this.shapeLimitations.leftMax.y) this.shapeValues.leftCells.y = this.shapeLimitations.leftMax.y;
            if (this.shapeValues.leftCells.x > this.shapeLimitations.leftMax.x) this.shapeValues.leftCells.x = this.shapeLimitations.leftMax.x;
            if (this.shapeValues.rightCells.y > this.shapeLimitations.rightMax.y) this.shapeValues.rightCells.y = this.shapeLimitations.rightMax.y;
            if (this.shapeValues.rightCells.x > this.shapeLimitations.rightMax.x) this.shapeValues.rightCells.x = this.shapeLimitations.rightMax.x;
            if (this.shapeValues.doorCells.y > this.shapeLimitations.doorMax.y) {
                this.shapeValues.doorCells.y = this.shapeLimitations.doorMax.y;
                if (this.input.totalHeight > this.shapeLimitations.doorMax.y && this.shapeLimitations.allowTop)
                {
                    this.shapeValues.isSkylightEnabled = true;
                    this.shapeValues.skylightCells.y = 1;
                }
            }
            if (this.shapeValues.doorCells.x > this.shapeLimitations.doorMax.x) {
                this.shapeValues.doorCells.x = this.shapeLimitations.doorMax.x;
            }
            if (this.shapeValues.skylightCells.y > this.shapeLimitations.topMax.y) this.shapeValues.skylightCells.y = this.shapeLimitations.topMax.y;
            if (this.shapeValues.skylightCells.x > this.shapeLimitations.topMax.x) this.shapeValues.skylightCells.x = this.shapeLimitations.topMax.x;
        },
        updateInput() {

            this.input.totalHeight = this.grid.y;
            this.input.doorWidth = this.shapeValues.doorCells.x;
            this.input.totalWidth = this.grid.x;
            this.input.leftWidth = this.shapeValues.leftCells.x;
            this.input.rightWidth = this.shapeValues.rightCells.x;
        },

        async sendData(el, redirect) {
            this.loading=true;
            try {
                const r = await fetch('', {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        'styleLine': this.styleLineDesc,
                        'color1': this.color1Desc,
                        'usecase': this.productUsecaseDesc,
                        'type': this.productTypeDesc,
                        'additivies': this.additivesDesc,
                        'color2': this.color2Desc,
                        'smart': this.smartHomeDesc,
                        'sideLimitation': this.shapeLimitations.sides[0],
                        'doorSide': this.shapeValues.doorSide,
                        'leftWindowEnabled': this.shapeValues.isWindowsLeftEnabled,
                        'rightWindowEnabled': this.shapeValues.isWindowsRightEnabled,
                        'topWindowEnabled': this.shapeValues.isSkylightEnabled,
                        'productWidth': this.input.totalWidth,
                        'productHeight': this.input.totalHeight,
                        'doorWidth': this.input.doorWidth,
                        'rightWidth': this.input.rightWidth,
                        'leftWidth': this.input.leftWidth,
                    })
                })
                if (!r.ok) throw r;
                return await r.json();
            } finally {
                this.loading=false;
                if (redirect) window.location.href = el.dataset.url;
            }
        },

        initStep3() {
            const step_3_slides = document.querySelectorAll('.selection__element.step-3')
            const step_3_dots = document.querySelectorAll('.dots.step-3 > .dynamic > .dot')
            const step_3_observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if(entry.isIntersecting) {
                        const index = [...step_3_slides].indexOf(entry.target);
                        step_3_dots.forEach(dot => dot.classList.remove('active'));
                        step_3_dots[index].classList.add('active');
                    }
                });
            },{
                root: document.querySelector('.selection.step-3'),
                threshold: 0.6,
            });

            step_3_slides.forEach(slide => step_3_observer.observe(slide));

        },
        initSlider(range)
        {
            requestAnimationFrame(() => this.updateSlider(range));
        },
        updateSlider(range)
        {
            const min = parseFloat(range.min);
            const max = parseFloat(range.max);
            const val = parseFloat(range.value);

            const percent = ((val - min) * 100) / (max - min);
            range.style.setProperty('--range-value', `${percent}%`);
        },

        initStep5() {
            const step_5_slides = document.querySelectorAll('.selection__element.step-5')
            const step_5_dots = document.querySelectorAll('.dots.step-5 > .dynamic > .dot')
            const step_5_observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if(entry.isIntersecting) {
                        const index = [...step_5_slides].indexOf(entry.target);
                        step_5_dots.forEach(dot => dot.classList.remove('active'));
                        step_5_dots[index].classList.add('active');
                    }
                });
            },{
                root: document.querySelector('.selection.step-5'),
                threshold: 0.6,
            });


            step_5_slides.forEach(slide => step_5_observer.observe(slide));

        }
    }
}
