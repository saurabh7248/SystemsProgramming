import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.Font;
import java.awt.Toolkit;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
public class Notepad extends JFrame {
	JPanel panel;
	JMenuBar menuBar;
	JMenu fileMenu,formatMenu,fontMenu,sizeMenu;
	JMenuItem openItem,newItem,saveItem,saveasItem,exitItem,backgroundItem,foregroundItem,cutItem,copyItem,pasteItem,arialItem,timeNewRomanItem,boldItem,italicItem;
	JEditorPane textArea;
	JPopupMenu rightClickMenu;
	File document;
	boolean saved;
	public Notepad() {
		this.saved = true;
		this.setTitle("Notepad");
		Toolkit toolkit = Toolkit.getDefaultToolkit();
		Dimension Screen = toolkit.getScreenSize();
		this.setSize(Screen.width / 2, Screen.height / 2);
		this.setVisible(true);
		this.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		this.setLocation(Screen.width / 4, Screen.height / 4);
		menuBar = new JMenuBar();
		fileMenu = new JMenu("File");
		formatMenu = new JMenu("Format");
		fontMenu = new JMenu("Font");
		sizeMenu=new JMenu("Size");
		menuBar.add(fileMenu);
		menuBar.add(formatMenu);
		this.setJMenuBar(menuBar);
		openItem = new JMenuItem("Open");
		newItem = new JMenuItem("New");
		saveItem = new JMenuItem("Save");
		saveasItem = new JMenuItem("Save As");
		exitItem = new JMenuItem("Exit");
		backgroundItem = new JMenuItem("Background");
		foregroundItem = new JMenuItem("Foreground");
		textArea = new JEditorPane();
		rightClickMenu = new JPopupMenu();
		cutItem = new JMenuItem("Cut");
		pasteItem = new JMenuItem("Paste");
		copyItem = new JMenuItem("Copy");
		arialItem = new JMenuItem("Arial");
		timeNewRomanItem = new JMenuItem("Times New Roman");
		boldItem = new JMenuItem("Bold");
		italicItem = new JMenuItem("Italic");
		fontMenu.add(arialItem);
		fontMenu.add(timeNewRomanItem);
		fontMenu.addSeparator();
		fontMenu.add(boldItem);
		fontMenu.add(italicItem);
		this.add(textArea);
		fileMenu.add(newItem);
		fileMenu.addSeparator();
		fileMenu.add(openItem);
		fileMenu.add(saveItem);
		fileMenu.add(saveasItem);
		fileMenu.addSeparator();
		fileMenu.add(exitItem);
		formatMenu.add(backgroundItem);
		formatMenu.add(foregroundItem);
		formatMenu.addSeparator();
		formatMenu.add(fontMenu);
		formatMenu.addSeparator();
		formatMenu.add(sizeMenu);
		rightClickMenu.add(cutItem);
		rightClickMenu.add(pasteItem);
		rightClickMenu.add(copyItem);
		exitItem.addActionListener(new ExitHandler());
		this.addWindowListener(new CrossHandler());
		newItem.addActionListener(new NewHandler());
		openItem.addActionListener(new OpenHandler());
		saveItem.addActionListener(new SaveHandler());
		saveasItem.addActionListener(new SaveAsHandler());
		textArea.addMouseListener(new RightClickHandler());
		textArea.addKeyListener(new RightClickHandler());
		cutItem.addActionListener(new CutHandler());
		pasteItem.addActionListener(new PasteHandler());
		copyItem.addActionListener(new CopyHandler());
		backgroundItem.addActionListener(new BackgroundHandler());
		foregroundItem.addActionListener(new ForegroundHandler());
		arialItem.addActionListener(new FontHandler("Arial"));
		timeNewRomanItem.addActionListener(new FontHandler("Times New Roman"));
		boldItem.addActionListener(new BoldHandler());
		italicItem.addActionListener(new ItalicHandler());
		textArea.add(new JScrollBar());
		sizeMenu.add(new FontSizeMenuItem(12));
		sizeMenu.add(new FontSizeMenuItem(14));
		sizeMenu.add(new FontSizeMenuItem(16));
		sizeMenu.add(new FontSizeMenuItem(18));
	}
	public class ExitHandler implements ActionListener{
		public void actionPerformed(ActionEvent arg0) {
			Notepad.this.dispose();
		}
	}
	public class NewHandler implements ActionListener{
		public void actionPerformed(ActionEvent arg0) {
			new Notepad();
		}
	}
	public class CrossHandler implements WindowListener{
		public void windowActivated(WindowEvent arg0) {
		}
		public void windowClosed(WindowEvent arg0) {
			if(Notepad.this.saved!=true){
				new YesNoDialog();
			}
		}
		public void windowClosing(WindowEvent arg0) {
		}
		public void windowDeactivated(WindowEvent arg0) {
		}
		public void windowDeiconified(WindowEvent arg0) {
		}
		public void windowIconified(WindowEvent arg0) {
		}
		public void windowOpened(WindowEvent arg0) {
		}
	}
	public class OpenHandler implements ActionListener{
		public void actionPerformed(ActionEvent arg0) {
				int selected;
				JFileChooser selectFile=new JFileChooser();
				FileNameExtensionFilter filterText=new FileNameExtensionFilter("Text Files","txt");
				selectFile.setFileFilter(filterText);
				selected=selectFile.showOpenDialog(new JFrame());
				if(selected==JFileChooser.APPROVE_OPTION){
					Notepad.this.setTitle(selectFile.getSelectedFile().getName()+"-Notepad");
					Notepad.this.document=selectFile.getSelectedFile();
					Notepad.this.saved=true;
					try {
						Notepad.this.textArea.read(new FileInputStream(document),selectFile.getDescription(document));
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
		}
	}
	public class SaveHandler implements ActionListener{
		public void actionPerformed(ActionEvent arg0) {
			if(Notepad.this.document ==null){
				int selected;
				JFileChooser selectFile=new JFileChooser();
				FileNameExtensionFilter filterText=new FileNameExtensionFilter("Text File","txt");
				selectFile.setFileFilter(filterText);
				selected=selectFile.showSaveDialog(new JFrame());
				if(selected==JFileChooser.APPROVE_OPTION){
					try {
						Notepad.this.textArea.write(new FileWriter(selectFile.getSelectedFile()));
						Notepad.this.document=selectFile.getSelectedFile();
						Notepad.this.setTitle(selectFile.getSelectedFile().getName()+"-Notepad");
						Notepad.this.saved=true;
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			}
			else{
				try {
					Notepad.this.textArea.write(new FileWriter(document));
					Notepad.this.saved=true;
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}
	public class SaveAsHandler implements ActionListener{
		public void actionPerformed(ActionEvent arg0) {
			int selected;
			JFileChooser selectFile=new JFileChooser();
			FileNameExtensionFilter filterText=new FileNameExtensionFilter("Text File","txt");
			selectFile.setFileFilter(filterText);
			selected=selectFile.showSaveDialog(new JFrame());
			if(selected==JFileChooser.APPROVE_OPTION){
				try {
					Notepad.this.textArea.write(new FileWriter(selectFile.getSelectedFile()));
					Notepad.this.document=selectFile.getSelectedFile();
					Notepad.this.saved=true;
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}		
	}
	public class RightClickHandler implements MouseListener,KeyListener{
		public void mouseClicked(MouseEvent event) {
			if(event.isPopupTrigger())
			{
				Notepad.this.rightClickMenu.show(true);
				Notepad.this.setTitle("Saurabh");;
			}
		}
		public void mouseEntered(MouseEvent event) {
		}
		public void mouseExited(MouseEvent event) {
		}
		public void mousePressed(MouseEvent event) {
			if(event.isPopupTrigger())
			{
				Notepad.this.rightClickMenu.show(true);
			}
		}
		public void mouseReleased(MouseEvent event) {	
			if(event.isPopupTrigger())
			{
				Notepad.this.rightClickMenu.show(textArea, event.getX(), event.getY());
			}
		}
		public void keyPressed(KeyEvent arg0) {
			Notepad.this.saved=false;
		}
		public void keyReleased(KeyEvent arg0) {
			Notepad.this.saved=false;
		}
		public void keyTyped(KeyEvent arg0) {
			Notepad.this.saved=false;
		}		
	}
	public class CutHandler implements ActionListener{
		public void actionPerformed(ActionEvent arg0) {
			Notepad.this.textArea.cut();
		}
	}
	public class CopyHandler implements ActionListener{
		public void actionPerformed(ActionEvent e) {
			Notepad.this.textArea.copy();
		}
	}
	public class PasteHandler implements ActionListener{
		public void actionPerformed(ActionEvent e) {
			Notepad.this.textArea.paste();
		}
	}
	public class BackgroundHandler implements ActionListener,ChangeListener{
		JFrame temp=new JFrame("Choose a background color");
		JColorChooser colorChooser=new JColorChooser(Notepad.this.textArea.getBackground());
		public BackgroundHandler(){
			temp.setSize(500,325);
			Toolkit kit=Toolkit.getDefaultToolkit();
			Dimension dim=kit.getScreenSize();
			temp.setLocation(dim.width/2-250,dim.height/2-162);
		}
		public void stateChanged(ChangeEvent arg0) {
			Notepad.this.textArea.setBackground(colorChooser.getColor());
		}
		public void actionPerformed(ActionEvent arg0) {
			temp.add(colorChooser);
			temp.show();
			colorChooser.getSelectionModel().addChangeListener(this);
		}
	}
	public class ForegroundHandler implements ActionListener,ChangeListener{
		JFrame temp=new JFrame("Choose a foreground color");
		JColorChooser colorChooser=new JColorChooser(Notepad.this.textArea.getForeground());
		public ForegroundHandler(){
			temp.setSize(500,325);
			Toolkit kit=Toolkit.getDefaultToolkit();
			Dimension dim=kit.getScreenSize();
			temp.setLocation(dim.width/2-250,dim.height/2-162);
		}
		public void stateChanged(ChangeEvent arg0) {
			Notepad.this.textArea.setForeground(colorChooser.getColor());
		}
		public void actionPerformed(ActionEvent arg0) {
			temp.show();
			temp.add(colorChooser);
			colorChooser.getSelectionModel().addChangeListener(this);
		}
	}
	public class FontHandler implements ActionListener{
		String fontName;
		public FontHandler(String fontName){
			this.fontName=fontName;
		}
		public void actionPerformed(ActionEvent arg0) {
			Font font=new Font(fontName,Notepad.this.textArea.getFont().getStyle(),Notepad.this.textArea.getFont().getSize());
			Notepad.this.textArea.setFont(font);
		}
	}
	public class BoldHandler implements ActionListener{
		public void actionPerformed(ActionEvent arg0) {
			if(Notepad.this.textArea.getFont().isBold()){
				Notepad.this.textArea.setFont(Notepad.this.textArea.getFont().deriveFont(Notepad.this.textArea.getFont().getStyle()-Font.BOLD));
			}
			else{
				Notepad.this.textArea.setFont(Notepad.this.textArea.getFont().deriveFont(Notepad.this.textArea.getFont().getStyle()+Font.BOLD));
			}
		}
	}
	public class ItalicHandler implements ActionListener{
		public void actionPerformed(ActionEvent arg0) {
			if(Notepad.this.textArea.getFont().isItalic()){
				Notepad.this.textArea.setFont(Notepad.this.textArea.getFont().deriveFont(Notepad.this.textArea.getFont().getStyle()-Font.ITALIC));
			}
			else{
				Notepad.this.textArea.setFont(Notepad.this.textArea.getFont().deriveFont(Notepad.this.textArea.getFont().getStyle()+Font.ITALIC));
			}
		}
	}
	public class YesNoDialog extends JFrame{
		public YesNoDialog(){
			JLabel label=new JLabel("Do you want to save this file");
			JPanel panel=new JPanel();
			this.add(panel);
			panel.add(label);
			JButton yesButton=new JButton("Yes");
			JButton noButton=new JButton("No");
			yesButton.addActionListener(new YesHandler());
			noButton.addActionListener(new NoHandler());
			this.setVisible(true);
			panel.add(yesButton);
			panel.add(noButton);
			Toolkit kit=Toolkit.getDefaultToolkit();
			Dimension dim=kit.getScreenSize();
			this.setSize(376,100);
			this.setLocation(dim.width/2-188,dim.height/2-50);
		}
		public class YesHandler implements ActionListener{
			public void actionPerformed(ActionEvent arg0) {
				if(Notepad.this.document!=null)
				{
					try {
						Notepad.this.textArea.write(new FileWriter(document));
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
				else{
					int selected;
					JFileChooser selectFile=new JFileChooser();
					FileNameExtensionFilter filterText=new FileNameExtensionFilter("Text File","txt");
					selectFile.setFileFilter(filterText);
					selected=selectFile.showSaveDialog(new JFrame());
					if(selected==JFileChooser.APPROVE_OPTION){
						try {
							Notepad.this.textArea.write(new FileWriter(selectFile.getSelectedFile()));
							Notepad.this.document=selectFile.getSelectedFile();
							Notepad.this.setTitle(selectFile.getSelectedFile().getName()+"-Notepad");
							Notepad.this.saved=true;
						} catch (IOException e) {
							e.printStackTrace();
						}
					}
				}
			}
		}
		public class NoHandler implements ActionListener{
			public void actionPerformed(ActionEvent arg0) {
				YesNoDialog.this.dispose();
			}
		}
	}
	public class FontSizeMenuItem extends JMenuItem{
		float size;
		public FontSizeMenuItem(int size){
			this.size=(float)size;
			this.addActionListener(new FontSizeHandler());
			this.setLabel(new Integer(size).toString());
		}
		public class FontSizeHandler implements ActionListener{
			public void actionPerformed(ActionEvent arg0) {
				Notepad.this.textArea.setFont(Notepad.this.textArea.getFont().deriveFont(FontSizeMenuItem.this.size));
			}			
		}
	}
}
