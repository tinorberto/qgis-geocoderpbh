# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeocoderPbh
                                 A QGIS plugin
 Geocoder PBH
                              -------------------
        begin                : 2017-02-07
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Prodabel
        email                : tinorberto@gmail.com.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from geocoder_dialog import GeocoderPbhDialog
import os.path
import json, requests

class GeocoderPbh:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GeocoderPbh_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GeocoderPBH')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'GeocoderPbh')
        self.toolbar.setObjectName(u'GeocoderPbh')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GeocoderPbh', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = GeocoderPbhDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)
		
        self.dlg.sendButton.clicked.connect(self.teste)

        return action
		
		
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GeocoderPbh/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Geocoder'),
            callback=self.run,
            parent=self.iface.mainWindow())
	


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&GeocoderPBH'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def teste(self):
        layer =  QgsVectorLayer('LineString', 'lines' , "memory")
        pr = layer.dataProvider() 
        # add the first point
        pt = QgsFeature()

        wkt = "[[-43.95213962016855, -19.86504771937976], [-43.9526015658137, -19.8645873285705], [-43.9526153448243, -19.8645996955951], [-43.9526292019921, -19.8646121534166], [-43.9518749500593, -19.8653639502302], [-43.9517577703675, -19.865476015818], [-43.9515110912197, -19.8657025587655], [-43.9511146152723, -19.8660558880949], [-43.95092089988, -19.8662410507331], [-43.9508444543573, -19.866291850481], [-43.9507869128157, -19.8662830785506], [-43.95075965202, -19.8662576171273], [-43.9507559179848, -19.8661998577136], [-43.9507583353233, -19.8654593228312], [-43.9507604940765, -19.8654499713874], [-43.9507630809054, -19.8654398823225], [-43.9507662024669, -19.8654289128662], [-43.9507699757061, -19.8654169677096], [-43.9507748715601, -19.865403065113], [-43.9507808686613, -19.8653878592663], [-43.9507882016162, -19.8653712874661], [-43.9507923596479, -19.8653626653639], [-43.9507968155696, -19.8653539402634], [-43.950802132422, -19.8653441329939], [-43.9508076830367, -19.8653345025322], [-43.9508133621763, -19.8653252088991], [-43.9508190792282, -19.8653163565043], [-43.9508246674994, -19.8653081378728], [-43.9508301570163, -19.8653004407269], [-43.9508406873526, -19.8652865993416], [-43.9508496802141, -19.8652756247819], [-43.9508581148571, -19.8652659534657], [-43.9508660031004, -19.865257398854], [-43.9508734281334, -19.8652497419275], [-43.9514767561274, -19.864708091292], [-43.9515087112341, -19.8646602331107], [-43.9516253628568, -19.8645494497787], [-43.9519362251902, -19.8643073423244], [-43.9520679553973, -19.8641785715615], [-43.9521333367636, -19.8640679299726], [-43.9521634570506, -19.8639783105846], [-43.9521874715905, -19.8638950693253], [-43.9521878293607, -19.8638290406153], [-43.9521875223436, -19.8637188352383], [-43.9521777619866, -19.8631571348394], [-43.9521768021399, -19.8630431697934], [-43.9521766672825, -19.8628303662334], [-43.9521787208012, -19.8625177166338], [-43.9521941941959, -19.8624399357861], [-43.9522093657841, -19.8624173575554], [-43.9523189660096, -19.8622517847189], [-43.9524821603996, -19.8619996923619], [-43.9526413105544, -19.8617483121427], [-43.952868182357, -19.8613653449187], [-43.9531433858563, -19.8609373113478], [-43.9532850878725, -19.8607524074479], [-43.9535849782464, -19.8602941643113], [-43.9536012151075, -19.8602199110117], [-43.9535909333251, -19.8601666411113], [-43.953589844548, -19.8601646411818], [-43.9534740196216, -19.8599386447871], [-43.9531220135195, -19.859191292345], [-43.9530765488986, -19.8590987332345], [-43.9528218478423, -19.8586152334072], [-43.9527778237301, -19.8585250705994], [-43.9525633815396, -19.8580416188295], [-43.9525180680856, -19.8579403281169], [-43.9523003170662, -19.8574581342523], [-43.9522554376536, -19.8573566075518], [-43.9520512579769, -19.8568723342994], [-43.9519951227755, -19.856743611308], [-43.951802418849, -19.8563190718842], [-43.9517030061636, -19.8561007843006], [-43.9515086087086, -19.8556757271368], [-43.951506160153, -19.8556617846359], [-43.9515052706612, -19.8556450600162], [-43.9515058105389, -19.8556348055634], [-43.9515073474701, -19.8556236385235], [-43.9515101426166, -19.8556116280785], [-43.9515143105641, -19.8555993228459], [-43.9515200348943, -19.8555868096968], [-43.9515267559289, -19.8555753726635], [-43.9515339128889, -19.8555654810949], [-43.951541201587, -19.8555570407671], [-43.9515543160138, -19.8555447491149], [-43.9515665260065, -19.8555357509397], [-43.9519080994147, -19.8553602065186], [-43.952058702337, -19.8552821697415], [-43.9522091119308, -19.855203361648], [-43.9522198612661, -19.855195280838], [-43.9522313510797, -19.8551842579324], [-43.9522376980218, -19.8551767049585], [-43.9522438946405, -19.8551678669888], [-43.952249666872, -19.8551576661263], [-43.952254525254, -19.8551465221978], [-43.9522580030617, -19.8551355514514], [-43.9522602531414, -19.855124854186], [-43.9522613885181, -19.8551149185894], [-43.9522616444408, -19.8551058062515], [-43.9522604617782, -19.8550909757381], [-43.9522579314614, -19.8550786478861], [-43.9522501175407, -19.8550626744134], [-43.9517604450917, -19.8541189133781], [-43.9517558213819, -19.8541046335276], [-43.9517523028425, -19.8540870787947], [-43.951751237961, -19.8540759208038], [-43.9517510920763, -19.8540635673423], [-43.9517521697676, -19.8540500834845], [-43.9517546615344, -19.8540361808521], [-43.9517582597434, -19.8540233631855], [-43.9517627765027, -19.8540115160119], [-43.9517678101193, -19.854001045484], [-43.9517731172901, -19.8539918634939], [-43.9517831722746, -19.8539777324554], [-43.9517929145678, -19.8539667364107], [-43.9521298369248, -19.8537368119868], [-43.9522647540285, -19.8536689958517], [-43.95229595588, -19.8536591562021], [-43.9523042657571, -19.8536561202894], [-43.9523137524736, -19.8536513159842], [-43.9523254171482, -19.8536429187142], [-43.9523366151182, -19.8536309048189], [-43.9523432259141, -19.8536203694356], [-43.952347376521, -19.8536107012538], [-43.9523508615698, -19.8535955535413], [-43.9522560759182, -19.8532648234318], [-43.9521849668325, -19.8530532520429], [-43.9521286753211, -19.8527860597779], [-43.9521472828269, -19.8527824652531]]";

        wkt = wkt.replace("[", "").replace("],", "*").replace(",", " ").replace("*", ",").replace("]]","")
        
        wkt = "LINESTRING ()" 
        
        response = requests.get("http://geocoder.pbh.gov.br/geocoder/v1/address?logradouro=afonso pena")
        print response.status_code
        print response.content
		
        print wkt;
        
        pt.setGeometry(QgsGeometry.fromWkt(wkt))
        pr.addFeatures([pt])
        # update extent of the layer
        layer.updateExtents()
        # add the layer to the canvas
        QgsMapLayerRegistry.instance().addMapLayers([layer])